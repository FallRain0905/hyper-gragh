"""Declarative identity registry compiler and exact lookup index.

The registry is intentionally deterministic and offline.  It validates YAML
once, builds an exact (never substring) alias index and exposes immutable
snapshots plus dependency-scoped hashes so unrelated registry edits do not
invalidate successful identity decisions.

Design rules enforced here:

* display names can change; ``canonical_id`` cannot be silently redefined;
* a surface form may have several candidates only when every declaration is
  explicitly scoped and the scopes cannot overlap;
* unreviewed migration suggestions are stored but never participate in
  runtime lookup unless a reviewer asks for them;
* component/formula containment is never treated as an alias;
* unknown fields, dangling references and redirect cycles fail at load time.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable, Mapping

import yaml
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)

from .contracts import (
    SCHEMA_VERSION,
    STRATEGY,
    CanonicalEntity,
    canonical_json,
    digest,
)
from .text_policy import default_normalizer_for_kind, normalize

_TOP_LEVEL_KEYS = frozenset(
    {
        "schema_version",
        "domain",
        "description",
        "entities",
        "units",
        "negative_pairs",
        "high_risk_groups",
        "redirects",
        "roles",
        "defaults",
    }
)


class RegistryError(ValueError):
    """Raised when declarative registry configuration is invalid."""


class NegativePair(BaseModel):
    model_config = ConfigDict(extra="forbid")

    left: str
    right: str
    reason: str = ""

    @field_validator("left", "right")
    @classmethod
    def _non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Negative pair IDs must be non-empty")
        return value


class HighRiskGroup(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    canonical_ids: list[str]
    reason: str = ""

    @field_validator("name")
    @classmethod
    def _name_non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("High-risk group name must be non-empty")
        return value

    @field_validator("canonical_ids")
    @classmethod
    def _ids_non_empty(cls, values: list[str]) -> list[str]:
        cleaned = [value for value in values if value and value.strip()]
        if not cleaned:
            raise ValueError("High-risk group requires canonical_ids")
        return sorted(set(cleaned))


class RoleDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    description: str = ""
    applies_to_kinds: list[str] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def _name_non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Role name must be non-empty")
        return value


class UnitDefinition(BaseModel):
    """One explicit unit conversion into a dimension's base unit."""

    model_config = ConfigDict(extra="forbid")

    symbol: str
    dimension: str
    factor: str
    base_unit: str | None = None
    offset: str = "0"
    aliases: list[str] = Field(default_factory=list)
    notes: str | None = None

    @field_validator("symbol", "dimension")
    @classmethod
    def _non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Unit symbol/dimension must be non-empty")
        return value

    @field_validator("factor", "offset", mode="before")
    @classmethod
    def _decimal_string(cls, value: Any) -> str:
        if isinstance(value, bool):
            raise ValueError("Unit factor/offset must be numeric")
        if isinstance(value, (int, float, Decimal)):
            value = str(value)
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Unit factor/offset must be a decimal string")
        try:
            parsed = Decimal(value)
        except InvalidOperation as exc:
            raise ValueError(f"Invalid decimal value {value!r}") from exc
        if not parsed.is_finite():
            raise ValueError("Unit factor/offset must be finite")
        return format(parsed, "f")

    @field_validator("aliases")
    @classmethod
    def _aliases(cls, values: list[str]) -> list[str]:
        return sorted({value for value in values if value and value.strip()})

    @model_validator(mode="after")
    def _validate_scale(self) -> "UnitDefinition":
        if Decimal(self.factor) <= 0:
            raise ValueError("Unit conversion factor must be positive")
        return self


@dataclass(frozen=True)
class AliasBinding:
    entity_id: str
    text: str
    normalized: str
    normalizer: str
    kind: str
    scope: Any
    guards: tuple[tuple[str, str], ...]
    granularity: str
    review_status: str
    source: str
    ambiguous: bool = False


@dataclass(frozen=True)
class UnitAlias:
    symbol: str
    alias: str


def _scope_key(scope: Any) -> str:
    return canonical_json(scope)


def _scope_alternatives(scope: Any) -> list[Any] | None:
    if scope is None:
        return [None]
    if isinstance(scope, list):
        return list(scope)
    return [scope]


def _scope_matches(alias_scope: Any, query_scope: Any) -> bool:
    """Return whether a query scope satisfies an alias scope constraint."""

    if alias_scope is None:
        return True
    if query_scope is None:
        return False
    for alternative in _scope_alternatives(alias_scope):
        if isinstance(alternative, str):
            if isinstance(query_scope, str) and query_scope == alternative:
                return True
            if isinstance(query_scope, Mapping):
                for key in ("doc_id", "document", "scope"):
                    if query_scope.get(key) == alternative:
                        return True
                    if isinstance(query_scope.get(key), (list, tuple, set)) and alternative in query_scope[key]:
                        return True
        elif isinstance(alternative, Mapping):
            if isinstance(query_scope, Mapping):
                if all(query_scope.get(key) == value for key, value in alternative.items()):
                    return True
    return False


def _scopes_overlap(left: Any, right: Any) -> bool:
    left_options = _scope_alternatives(left)
    right_options = _scope_alternatives(right)
    for left_option in left_options:
        for right_option in right_options:
            if left_option is None or right_option is None:
                return True
            if isinstance(left_option, str) and isinstance(right_option, str):
                if left_option == right_option:
                    return True
                continue
            if isinstance(left_option, Mapping) and isinstance(right_option, Mapping):
                shared = set(left_option) & set(right_option)
                if all(left_option[key] == right_option[key] for key in shared):
                    return True
                continue
            if _scope_matches(left_option, right_option) or _scope_matches(
                right_option, left_option
            ):
                return True
    return False


def _entity_semantic(entity: CanonicalEntity) -> dict[str, Any]:
    payload = entity.model_dump(mode="json")
    payload["aliases"] = sorted(payload["aliases"], key=canonical_json)
    payload["scoped_aliases"] = sorted(payload["scoped_aliases"], key=canonical_json)
    payload["identity_guards"] = sorted(payload["identity_guards"])
    payload["variant_dimensions"] = sorted(payload["variant_dimensions"])
    return payload


class Registry:
    """Compiled immutable view of one or more declarative YAML files."""

    def __init__(
        self,
        entities: Iterable[CanonicalEntity],
        *,
        units: Iterable[UnitDefinition] = (),
        negative_pairs: Iterable[NegativePair] = (),
        high_risk_groups: Iterable[HighRiskGroup] = (),
        redirects: Mapping[str, str] | None = None,
        roles: Iterable[RoleDefinition] = (),
        defaults: Mapping[str, Any] | None = None,
        source_paths: Iterable[str] = (),
    ) -> None:
        self.entities: dict[str, CanonicalEntity] = {}
        self.negative_pairs: tuple[NegativePair, ...] = ()
        self.high_risk_groups: tuple[HighRiskGroup, ...] = ()
        self.roles: tuple[RoleDefinition, ...] = ()
        self.defaults: dict[str, Any] = dict(defaults or {})
        self.sources: tuple[str, ...] = tuple(sorted(str(path) for path in source_paths))
        self.suggestions: tuple[AliasBinding, ...] = ()
        self.redirects: dict[str, str] = {}

        for entity in entities:
            existing = self.entities.get(entity.canonical_id)
            if existing is not None:
                if _entity_semantic(existing) != _entity_semantic(entity):
                    raise RegistryError(
                        f"Conflicting definitions for canonical_id {entity.canonical_id!r}"
                    )
                continue
            self.entities[entity.canonical_id] = entity

        if not self.entities:
            raise RegistryError("Registry requires at least one canonical entity")

        self._validate_redirects(redirects or {})
        self._validate_references(negative_pairs, high_risk_groups)
        self._validate_roles(roles)
        self._validate_units(units)
        self._build_index()
        self.snapshot_hash = self._compute_snapshot_hash()

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @classmethod
    def from_paths(cls, paths: Iterable[str | Path] | str | Path) -> "Registry":
        if isinstance(paths, (str, Path)):
            paths = [paths]
        files: list[Path] = []
        for raw_path in paths:
            path = Path(raw_path)
            if path.is_dir():
                files.extend(sorted(path.glob("*.yaml")))
                files.extend(sorted(path.glob("*.yml")))
            elif path.is_file():
                files.append(path)
            else:
                raise RegistryError(f"Registry path does not exist: {path}")
        unique_files = sorted({path.resolve() for path in files})
        if not unique_files:
            raise RegistryError("No registry YAML files found")

        entities: list[CanonicalEntity] = []
        seen: dict[str, tuple[CanonicalEntity, str]] = {}
        units: list[UnitDefinition] = []
        negative_pairs: list[NegativePair] = []
        high_risk_groups: list[HighRiskGroup] = []
        redirects: dict[str, str] = {}
        roles: list[RoleDefinition] = []
        defaults: dict[str, Any] = {}

        for path in unique_files:
            payload = cls._read_yaml(path)
            raw_entities = payload.get("entities") or []
            if not isinstance(raw_entities, list):
                raise RegistryError(f"{path}: entities must be a list")
            for raw_entity in raw_entities:
                try:
                    entity = CanonicalEntity.model_validate(raw_entity)
                except ValidationError as exc:
                    raise RegistryError(f"{path}: invalid entity: {exc}") from exc
                previous = seen.get(entity.canonical_id)
                if previous is not None:
                    previous_entity, previous_source = previous
                    if _entity_semantic(previous_entity) != _entity_semantic(entity):
                        raise RegistryError(
                            f"{path}: canonical_id {entity.canonical_id!r} conflicts with "
                            f"the definition in {previous_source}"
                        )
                    continue
                seen[entity.canonical_id] = (entity, str(path))
                entities.append(entity)

            for raw_unit in payload.get("units") or []:
                try:
                    units.append(UnitDefinition.model_validate(raw_unit))
                except ValidationError as exc:
                    raise RegistryError(f"{path}: invalid unit: {exc}") from exc

            for raw_pair in payload.get("negative_pairs") or []:
                try:
                    negative_pairs.append(NegativePair.model_validate(raw_pair))
                except ValidationError as exc:
                    raise RegistryError(f"{path}: invalid negative pair: {exc}") from exc

            for raw_group in payload.get("high_risk_groups") or []:
                try:
                    high_risk_groups.append(HighRiskGroup.model_validate(raw_group))
                except ValidationError as exc:
                    raise RegistryError(f"{path}: invalid high-risk group: {exc}") from exc

            raw_redirects = payload.get("redirects") or {}
            if not isinstance(raw_redirects, Mapping):
                raise RegistryError(f"{path}: redirects must be a mapping")
            for source, target in raw_redirects.items():
                if source in redirects and redirects[source] != target:
                    raise RegistryError(f"{path}: conflicting redirect for {source!r}")
                redirects[str(source)] = str(target)

            raw_roles = payload.get("roles") or []
            for raw_role in raw_roles:
                if isinstance(raw_role, str):
                    raw_role = {"name": raw_role}
                try:
                    roles.append(RoleDefinition.model_validate(raw_role))
                except ValidationError as exc:
                    raise RegistryError(f"{path}: invalid role: {exc}") from exc

            raw_defaults = payload.get("defaults") or {}
            if not isinstance(raw_defaults, Mapping):
                raise RegistryError(f"{path}: defaults must be a mapping")
            for key, value in raw_defaults.items():
                if key in defaults and defaults[key] != value:
                    raise RegistryError(f"{path}: conflicting default {key!r}")
                defaults[key] = value

        return cls(
            entities,
            units=units,
            negative_pairs=negative_pairs,
            high_risk_groups=high_risk_groups,
            redirects=redirects,
            roles=roles,
            defaults=defaults,
            source_paths=[str(path) for path in unique_files],
        )

    @staticmethod
    def _read_yaml(path: Path) -> Mapping[str, Any]:
        try:
            payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            raise RegistryError(f"{path}: cannot read YAML: {exc}") from exc
        if payload is None:
            payload = {}
        if not isinstance(payload, Mapping):
            raise RegistryError(f"{path}: top-level YAML value must be a mapping")
        unknown = set(payload) - _TOP_LEVEL_KEYS
        if unknown:
            raise RegistryError(f"{path}: unknown top-level fields: {sorted(unknown)}")
        version = payload.get("schema_version")
        if version != SCHEMA_VERSION:
            raise RegistryError(
                f"{path}: schema_version must be {SCHEMA_VERSION!r}, got {version!r}"
            )
        return payload

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def resolve_id(self, canonical_id: str) -> str:
        return self.redirects.get(canonical_id, canonical_id)

    def _validate_redirects(self, declared: Mapping[str, str]) -> None:
        merged = dict(declared)
        for entity in self.entities.values():
            if entity.redirect_to:
                existing = merged.get(entity.canonical_id)
                if existing is not None and existing != entity.redirect_to:
                    raise RegistryError(
                        f"Conflicting redirect for {entity.canonical_id!r}"
                    )
                merged[entity.canonical_id] = entity.redirect_to

        for source, target in merged.items():
            if source not in self.entities:
                raise RegistryError(f"Redirect source {source!r} is not a declared entity")
            if target not in self.entities:
                raise RegistryError(
                    f"Redirect {source!r} points to unknown entity {target!r}"
                )
            if source == target:
                raise RegistryError(f"Redirect cycle at {source!r}")

        for start in merged:
            seen: list[str] = []
            current = start
            while current in merged:
                if current in seen:
                    cycle = " -> ".join([*seen, current])
                    raise RegistryError(f"Redirect cycle: {cycle}")
                seen.append(current)
                current = merged[current]
        self.redirects = merged

    def _validate_references(
        self,
        negative_pairs: Iterable[NegativePair],
        high_risk_groups: Iterable[HighRiskGroup],
    ) -> None:
        for entity in self.entities.values():
            if entity.parent_id:
                target = self.resolve_id(entity.parent_id)
                if target not in self.entities:
                    raise RegistryError(
                        f"Entity {entity.canonical_id!r} has unknown parent "
                        f"{entity.parent_id!r}"
                    )
            if entity.redirect_to:
                if self.resolve_id(entity.redirect_to) not in self.entities:
                    raise RegistryError(
                        f"Entity {entity.canonical_id!r} redirects to an unknown entity"
                    )

        unique_pairs: dict[tuple[str, str], NegativePair] = {}
        for pair in negative_pairs:
            left = self.resolve_id(pair.left)
            right = self.resolve_id(pair.right)
            for identifier in (left, right):
                if identifier not in self.entities:
                    raise RegistryError(
                        f"Negative pair references unknown entity {identifier!r}"
                    )
            if left == right:
                raise RegistryError(
                    f"Negative pair {pair.left!r}/{pair.right!r} resolves to one identity"
                )
            key = tuple(sorted((left, right)))
            unique_pairs.setdefault(key, pair)
        self.negative_pairs = tuple(
            sorted(unique_pairs.values(), key=lambda item: (item.left, item.right))
        )

        groups: dict[str, HighRiskGroup] = {}
        for group in high_risk_groups:
            resolved = sorted({self.resolve_id(value) for value in group.canonical_ids})
            for identifier in resolved:
                if identifier not in self.entities:
                    raise RegistryError(
                        f"High-risk group {group.name!r} references unknown entity "
                        f"{identifier!r}"
                    )
            payload = group.model_copy(update={"canonical_ids": resolved})
            existing = groups.get(group.name)
            if existing is not None and existing.canonical_ids != resolved:
                raise RegistryError(
                    f"High-risk group {group.name!r} has conflicting members"
                )
            groups[group.name] = payload
        self.high_risk_groups = tuple(groups[name] for name in sorted(groups))

    def _validate_roles(self, roles: Iterable[RoleDefinition]) -> None:
        by_name: dict[str, RoleDefinition] = {}
        for role in roles:
            existing = by_name.get(role.name)
            if existing is not None and existing != role:
                raise RegistryError(f"Conflicting role definition for {role.name!r}")
            by_name[role.name] = role
        self.roles = tuple(by_name[name] for name in sorted(by_name))

    def _validate_units(self, units: Iterable[UnitDefinition]) -> None:
        by_symbol: dict[str, UnitDefinition] = {}
        alias_to_symbol: dict[str, str] = {}
        for unit in units:
            existing = by_symbol.get(unit.symbol)
            if existing is not None:
                if existing != unit:
                    raise RegistryError(f"Conflicting unit definition for {unit.symbol!r}")
                continue
            by_symbol[unit.symbol] = unit
            for alias in {unit.symbol, *unit.aliases}:
                previous = alias_to_symbol.get(alias)
                if previous is not None and previous != unit.symbol:
                    raise RegistryError(
                        f"Unit alias {alias!r} is declared by both {previous!r} and "
                        f"{unit.symbol!r}"
                    )
                alias_to_symbol[alias] = unit.symbol
        self.units: dict[str, UnitDefinition] = {
            symbol: by_symbol[symbol] for symbol in sorted(by_symbol)
        }
        self.unit_aliases: dict[str, str] = {
            alias: alias_to_symbol[alias] for alias in sorted(alias_to_symbol)
        }
        for unit in self.units.values():
            if unit.base_unit is not None:
                base = self.units.get(unit.base_unit)
                if base is None or base.dimension != unit.dimension or Decimal(base.factor) != 1 or Decimal(base.offset) != 0:
                    raise RegistryError("Unit base must name an explicit same-dimension unit with factor=1 and offset=0")

    def resolve_unit(self, name: str) -> UnitDefinition | None:
        symbol = self.unit_aliases.get(name)
        return self.units.get(symbol) if symbol else None

    # ------------------------------------------------------------------
    # Alias index
    # ------------------------------------------------------------------

    def _binding_from_alias(
        self,
        entity: CanonicalEntity,
        text: str,
        normalizer: str,
        *,
        scope: Any,
        guards: Mapping[str, Any],
        kind: str | None,
        granularity: str | None,
        review_status: str,
        source: str,
        ambiguous: bool = False,
    ) -> AliasBinding:
        normalized = normalize(text, normalizer)
        if not normalized:
            raise RegistryError(
                f"Entity {entity.canonical_id!r} declares an empty alias {text!r}"
            )
        guard_items = tuple(
            sorted((str(key), canonical_json(value)) for key, value in guards.items())
        )
        return AliasBinding(
            entity_id=entity.canonical_id,
            text=text,
            normalized=normalized,
            normalizer=normalizer,
            kind=kind or entity.kind,
            scope=scope,
            guards=guard_items,
            granularity=granularity or entity.granularity,
            review_status=review_status,
            source=source,
            ambiguous=ambiguous,
        )

    def _build_index(self) -> None:
        index: dict[str, dict[tuple[str, str], list[AliasBinding]]] = {}
        suggestions: list[AliasBinding] = []
        declared_scopes: dict[tuple[str, str, str, str], str] = {}

        for entity in self.entities.values():
            if entity.redirect_to or entity.status == "retired":
                continue
            default_normalizer = entity.name_normalizer or default_normalizer_for_kind(
                entity.kind
            )
            canonical = self._binding_from_alias(
                entity,
                entity.canonical_name,
                default_normalizer,
                scope=None,
                guards={},
                kind=entity.kind,
                granularity=entity.granularity,
                review_status="reviewed",
                source="canonical_name",
            )
            self._add_binding(index, suggestions, canonical, declared_scopes)

            for alias in [*entity.aliases, *entity.scoped_aliases]:
                binding = self._binding_from_alias(
                    entity,
                    alias.text,
                    alias.normalizer,
                    scope=alias.scope,
                    guards=alias.guards,
                    kind=alias.kind,
                    granularity=alias.granularity,
                    review_status=alias.review_status,
                    source="alias",
                    ambiguous=alias.ambiguous,
                )
                self._add_binding(index, suggestions, binding, declared_scopes)

        for normalizer, by_key in index.items():
            for key, bindings in by_key.items():
                entity_ids = {binding.entity_id for binding in bindings}
                if len(entity_ids) < 2:
                    continue
                for binding in bindings:
                    if binding.scope is None:
                        raise RegistryError(
                            "Conflicting unscoped alias declaration for "
                            f"{binding.text!r} (kind {binding.kind!r}); "
                            "scope every candidate or declare one identity"
                        )
                for position, left in enumerate(bindings):
                    for right in bindings[position + 1 :]:
                        if left.entity_id == right.entity_id:
                            continue
                        left_guards, right_guards = dict(left.guards), dict(right.guards)
                        disjoint_guards = any(name in right_guards and value != right_guards[name]
                                              for name, value in left_guards.items())
                        if _scopes_overlap(left.scope, right.scope) and not disjoint_guards and not (left.ambiguous and right.ambiguous):
                            raise RegistryError(
                                f"Overlapping scoped alias declarations for "
                                f"{left.text!r} between {left.entity_id!r} and "
                                f"{right.entity_id!r}"
                            )

        self._index = {
            normalizer: {
                key: tuple(sorted(bindings, key=lambda item: (item.entity_id, item.text)))
                for key, bindings in by_key.items()
            }
            for normalizer, by_key in index.items()
        }
        self.suggestions = tuple(
            sorted(suggestions, key=lambda item: (item.normalized, item.entity_id))
        )

    def _add_binding(
        self,
        index: dict[str, dict[tuple[str, str], list[AliasBinding]]],
        suggestions: list[AliasBinding],
        binding: AliasBinding,
        declared_scopes: dict[tuple[str, str, str, str], str],
    ) -> None:
        if binding.review_status != "reviewed":
            suggestions.append(binding)
            return
        key = (binding.normalized, binding.kind)
        bucket = index.setdefault(binding.normalizer, {}).setdefault(key, [])
        identity = (
            binding.normalizer,
            binding.normalized,
            binding.kind,
            binding.entity_id,
            _scope_key(binding.scope),
        )
        previous = declared_scopes.get(identity)
        if previous is not None:
            if previous != canonical_json(binding.guards):
                raise RegistryError(
                    f"Entity {binding.entity_id!r} declares conflicting guards for "
                    f"alias {binding.text!r}"
                )
            return
        declared_scopes[identity] = canonical_json(binding.guards)
        bucket.append(binding)

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def _entity_allows(
        self,
        entity: CanonicalEntity,
        *,
        kind: str,
        granularity: str,
        attributes: Mapping[str, Any],
    ) -> bool:
        if entity.status == "retired":
            return False
        if entity.kind != kind or entity.granularity != granularity:
            return False
        for guard in entity.identity_guards:
            if attributes.get(guard) is None or entity.properties.get(guard) is None or attributes[guard] != entity.properties.get(guard):
                # An unknown identity guard never proves that a mention is the
                # named variant.
                return False
        for dimension in entity.variant_dimensions:
            if dimension in attributes:
                if dimension not in entity.properties or attributes[dimension] != entity.properties[dimension]:
                    return False
        return True

    def lookup(
        self,
        raw_name: str,
        kind: str,
        scope: str | Mapping[str, Any] | None = None,
        attributes: Mapping[str, Any] | None = None,
        granularity: str = "concept",
        *,
        include_unreviewed: bool = False,
    ) -> list[CanonicalEntity]:
        """Return all identities whose declared key matches exactly.

        ``scope`` is matched against explicit alias scopes.  ``attributes``
        are checked against alias guards and the entity's identity guards.
        Missing attributes never establish sameness; they only fail to satisfy
        a required guard.  The result is sorted by ``canonical_id`` and has no
        hidden first-wins behaviour.
        """

        if not isinstance(raw_name, str) or not raw_name.strip():
            return []
        if not isinstance(kind, str) or not kind.strip():
            return []
        attributes = dict(attributes or {})

        found: dict[str, CanonicalEntity] = {}
        for normalizer, by_key in self._index.items():
            key = (normalize(raw_name, normalizer), kind)
            for binding in by_key.get(key, ()):
                if binding.granularity != granularity:
                    continue
                if not _scope_matches(binding.scope, scope):
                    continue
                if any(name not in attributes or attributes[name] is None or canonical_json(attributes[name]) != value for name, value in binding.guards):
                    continue
                target_id = self.resolve_id(binding.entity_id)
                entity = self.entities.get(target_id)
                if entity is None:
                    continue
                if not self._entity_allows(
                    entity,
                    kind=kind,
                    granularity=granularity,
                    attributes=attributes,
                ):
                    continue
                found[target_id] = entity

        if include_unreviewed:
            for binding in self.suggestions:
                key = (normalize(raw_name, binding.normalizer), kind)
                if key != (binding.normalized, binding.kind):
                    continue
                if binding.granularity != granularity:
                    continue
                if not _scope_matches(binding.scope, scope):
                    continue
                if any(name not in attributes or attributes[name] is None or canonical_json(attributes[name]) != value for name, value in binding.guards):
                    continue
                target_id = self.resolve_id(binding.entity_id)
                entity = self.entities.get(target_id)
                if entity is not None and self._entity_allows(
                    entity,
                    kind=kind,
                    granularity=granularity,
                    attributes=attributes,
                ):
                    found[target_id] = entity

        return [found[key] for key in sorted(found)]

    # ------------------------------------------------------------------
    # Hashing
    # ------------------------------------------------------------------

    def _compute_snapshot_hash(self) -> str:
        payload = {
            "schema_version": SCHEMA_VERSION,
            "strategy": STRATEGY,
            "entities": [
                _entity_semantic(self.entities[key]) for key in sorted(self.entities)
            ],
            "redirects": sorted(self.redirects.items()),
            "negative_pairs": sorted(
                (pair.model_dump(mode="json") for pair in self.negative_pairs),
                key=canonical_json,
            ),
            "high_risk_groups": sorted(
                (group.model_dump(mode="json") for group in self.high_risk_groups),
                key=canonical_json,
            ),
            "units": [
                self.units[key].model_dump(mode="json") for key in sorted(self.units)
            ],
            "roles": [role.model_dump(mode="json") for role in self.roles],
            "defaults": self.defaults,
        }
        return digest(payload)

    def dependency_hash(self, canonical_ids: Iterable[str]) -> str:
        """Return a hash over only the identities a decision depends on.

        Adding or editing an unrelated entity/alias does not change this value.
        """

        requested = sorted({str(value) for value in canonical_ids})
        if not requested:
            raise RegistryError("dependency_hash requires at least one canonical_id")
        resolved = sorted({self.resolve_id(value) for value in requested})
        for identifier in requested + resolved:
            if identifier not in self.entities:
                raise RegistryError(f"Unknown canonical_id {identifier!r}")

        resolved_set = set(resolved)
        entities = [_entity_semantic(self.entities[key]) for key in resolved]
        redirect_edges = sorted(
            (source, target)
            for source, target in self.redirects.items()
            if source in resolved_set or target in resolved_set
        )
        pairs = sorted(
            (
                pair.model_dump(mode="json")
                for pair in self.negative_pairs
                if self.resolve_id(pair.left) in resolved_set
                or self.resolve_id(pair.right) in resolved_set
            ),
            key=canonical_json,
        )
        groups = sorted(
            (
                group.model_dump(mode="json")
                for group in self.high_risk_groups
                if resolved_set & set(group.canonical_ids)
            ),
            key=canonical_json,
        )
        return digest(
            {
                "schema_version": SCHEMA_VERSION,
                "canonical_ids": requested,
                "entities": entities,
                "redirects": redirect_edges,
                "negative_pairs": pairs,
                "high_risk_groups": groups,
            }
        )

    def export(self, target: str | Path) -> str:
        """Write a reloadable frozen compiler input, without credentials."""
        target = Path(target)
        if target.exists():
            raise RegistryError("Registry export target already exists")
        payload = {"schema_version": SCHEMA_VERSION, "domain": "compiled_snapshot",
            "entities": [self.entities[key].model_dump(mode="json") for key in sorted(self.entities)],
            "units": [self.units[key].model_dump(mode="json") for key in sorted(self.units)],
            "negative_pairs": [pair.model_dump(mode="json") for pair in self.negative_pairs],
            "high_risk_groups": [group.model_dump(mode="json") for group in self.high_risk_groups],
            "roles": [role.model_dump(mode="json") for role in self.roles],
            "redirects": self.redirects, "defaults": self.defaults}
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
        restored = Registry.from_paths(target)
        if restored.snapshot_hash != self.snapshot_hash:
            raise RegistryError("Exported registry does not reproduce its semantic hash")
        return self.snapshot_hash
