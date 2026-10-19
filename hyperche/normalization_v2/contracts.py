"""Versioned offline-normalization contracts.

The records in this module are deliberately stricter than the legacy
normalization payloads.  They describe what a successful extraction *may*
hand to the offline stage; they never let an extraction model create a global
identity.  All source metadata that the extraction model does not control
(document, revision, chunk, prompt and profile hashes) is attached by code.

This module also owns the small configuration guards needed to keep a v2
job from accidentally becoming an online normalization job or from writing
into a source/accepted cache.
"""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Iterable, Literal, Mapping

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

SCHEMA_VERSION = "registry-offline-v2.1"
STRATEGY = "registry_offline_v2"

LEGACY_STRATEGIES = frozenset({"legacy_online", "legacy_posthoc"})
OFFLINE_PHASES = frozenset(
    {"offline", "posthoc", "post_extraction", "post-processing", "independent"}
)
ONLINE_PHASES = frozenset(
    {"online", "extraction", "during_extraction", "pre_extraction", "in_extraction"}
)
SUCCESS_FINISH_REASONS = frozenset(
    {"stop", "end_turn", "completed", "complete", "finished", "eos", "stop_sequence"}
)

Granularity = Literal["concept", "variant", "sample"]
NormalizerName = Literal["common_name", "chemical_formula", "exact"]
ReviewStatus = Literal["reviewed", "unreviewed", "migration_suggestion"]

PUBLISHED_MARKERS = (".published", "PUBLISHED", "published.json")
PUBLISHED_MANIFEST_STATUSES = frozenset({"published", "accepted", "validated"})


# ---------------------------------------------------------------------------
# Deterministic JSON, digests and identifiers
# ---------------------------------------------------------------------------


def _jsonable(value: Any) -> Any:
    """Convert supported Python values to a deterministic JSON value.

    ``sort_keys`` inside :func:`canonical_json` handles mappings; here we only
    normalise container/model types that the stdlib json encoder does not
    understand.  Unknown objects are rejected instead of being stringified,
    because a lossy ``str()`` would make fingerprints disagree silently.
    """

    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, Mapping):
        prepared: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("canonical_json only accepts string mapping keys")
            prepared[key] = _jsonable(item)
        return prepared
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, (set, frozenset)):
        prepared_items = [_jsonable(item) for item in value]
        return sorted(prepared_items, key=lambda item: json.dumps(item, sort_keys=True, ensure_ascii=False))
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise TypeError(f"Unsupported value for canonical JSON: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    """Return canonical, key-sorted, compact UTF-8 JSON."""

    return json.dumps(
        _jsonable(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    """Return the lowercase SHA256 hex digest of canonical JSON."""

    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def stable_id(prefix: str, value: Any) -> str:
    """Return a stable namespaced identifier.

    The digest is truncated to 32 hex characters so identifiers remain easy to
    store and print.  Uniqueness is checked by callers that persist new IDs.
    """

    if not isinstance(prefix, str) or not prefix.strip():
        raise ValueError("stable_id prefix must be a non-empty string")
    return f"{prefix}:{digest(value)[:32]}"


def utc_now() -> str:
    """Return current UTC time as an ISO-8601 ``Z`` timestamp."""

    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


# ---------------------------------------------------------------------------
# Shared validators
# ---------------------------------------------------------------------------


def _require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _dedupe(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


# ---------------------------------------------------------------------------
# Evidence
# ---------------------------------------------------------------------------


class EvidenceSpan(BaseModel):
    """An exact character span in one source chunk.

    Offsets are Python string offsets (Unicode code points), counted from the
    beginning of ``chunk.raw_text``.  A span is never inferred silently: the
    extraction adapter calls :func:`locate_evidence` and records a failure when
    the quote is absent or appears more than once without explicit offsets.
    """

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    quote: str = Field(min_length=1)
    start: int = Field(ge=0)
    end: int = Field(ge=0)
    chunk_id: str = Field(min_length=1)
    status: Literal["unverified", "verified"] = "unverified"

    @model_validator(mode="after")
    def _validate_shape(self) -> "EvidenceSpan":
        if self.end <= self.start:
            raise ValueError("Evidence span end must be greater than start")
        if self.end - self.start != len(self.quote):
            raise ValueError(
                "Evidence span offsets must describe exactly the quoted text "
                f"({self.end - self.start} offsets for {len(self.quote)} characters)"
            )
        return self


def locate_evidence(
    quote: str,
    text: str,
    chunk_id: str,
    *,
    start: int | None = None,
    end: int | None = None,
) -> EvidenceSpan:
    """Verify a quote, inferring offsets only when the match is unique.

    Explicit offsets are allowed to disambiguate a quote that occurs more than
    once.  A repeated quote without explicit offsets is rejected as ambiguous
    rather than resolved by picking the first occurrence.
    """

    _require_text(quote, "quote")
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    _require_text(chunk_id, "chunk_id")
    if (start is None) != (end is None):
        raise ValueError("Evidence offsets must be supplied together")

    if start is not None and end is not None:
        span = EvidenceSpan(quote=quote, start=start, end=end, chunk_id=chunk_id)
        return validate_evidence(span, text, chunk_id)

    occurrences: list[int] = []
    cursor = text.find(quote)
    while cursor != -1:
        occurrences.append(cursor)
        cursor = text.find(quote, cursor + 1)
    if not occurrences:
        raise ValueError("Evidence quote does not occur in the source chunk")
    if len(occurrences) > 1:
        raise ValueError(
            "Ambiguous evidence quote appears multiple times; explicit offsets are required"
        )
    span = EvidenceSpan(
        quote=quote,
        start=occurrences[0],
        end=occurrences[0] + len(quote),
        chunk_id=chunk_id,
    )
    return validate_evidence(span, text, chunk_id)


def validate_evidence(
    span: EvidenceSpan | Mapping[str, Any], text: str, chunk_id: str
) -> EvidenceSpan:
    """Return a verified copy of ``span`` or raise ``ValueError``.

    Rejects a chunk mismatch, out-of-bounds offsets and any span whose exact
    source characters differ from ``quote`` (including whitespace and Unicode
    differences).
    """

    parsed = span if isinstance(span, EvidenceSpan) else EvidenceSpan.model_validate(span)
    if parsed.chunk_id != chunk_id:
        raise ValueError("Evidence span belongs to a different chunk")
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    if parsed.end > len(text):
        raise ValueError("Evidence span extends beyond the source chunk")
    actual = text[parsed.start : parsed.end]
    if actual != parsed.quote:
        raise ValueError("Evidence span does not exactly match the source text")
    return parsed.model_copy(update={"status": "verified"})


# ---------------------------------------------------------------------------
# Mention / fact / batch
# ---------------------------------------------------------------------------


class Mention(BaseModel):
    """One name occurrence with its local meaning.

    ``kind`` is the object category (material, metric, process, ...), while
    ``roles`` are experimental roles (target, catalyst, adsorbent, ...).
    Keeping them separate prevents PTFE from becoming a new substance merely
    because a paper uses it as a binder in one experiment and a target in
    another.
    """

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    mention_id: str
    doc_id: str
    revision_hash: str
    chunk_id: str
    local_id: str
    raw_name: str
    kind: str
    roles: list[str] = Field(default_factory=list)
    granularity: Granularity = "concept"
    attributes: dict[str, Any] = Field(default_factory=dict)
    scope: dict[str, Any] = Field(default_factory=dict)
    evidence: list[EvidenceSpan] = Field(default_factory=list)
    aliases: list[str] = Field(default_factory=list)

    @field_validator(
        "mention_id",
        "doc_id",
        "revision_hash",
        "chunk_id",
        "local_id",
        "raw_name",
        "kind",
    )
    @classmethod
    def _non_empty(cls, value: str) -> str:
        return _require_text(value, "Mention field")

    @field_validator("roles")
    @classmethod
    def _valid_roles(cls, values: list[str]) -> list[str]:
        cleaned = [_require_text(value, "role") for value in values]
        return _dedupe(cleaned)

    @field_validator("aliases")
    @classmethod
    def _valid_aliases(cls, values: list[str]) -> list[str]:
        cleaned = [_require_text(value, "alias") for value in values]
        return _dedupe(cleaned)

    @model_validator(mode="after")
    def _evidence_matches_chunk(self) -> "Mention":
        for span in self.evidence:
            if span.chunk_id != self.chunk_id:
                raise ValueError("Mention evidence must belong to the mention chunk")
        return self


class RawFact(BaseModel):
    """A relation occurrence whose role members are local mention IDs."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    local_id: str
    relation_type: str
    roles: dict[str, list[str]]
    conditions: dict[str, Any] = Field(default_factory=dict)
    observations: list[dict[str, Any]] = Field(default_factory=list)
    evidence: list[EvidenceSpan] = Field(default_factory=list)
    context_id: str | None = None
    polarity: Literal["positive", "negative", "unspecified"] = "positive"
    assertion: Literal["reported", "measured", "hypothesized", "inferred"] = "reported"

    @field_validator("local_id", "relation_type")
    @classmethod
    def _non_empty(cls, value: str) -> str:
        return _require_text(value, "RawFact field")

    @field_validator("context_id")
    @classmethod
    def _optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _require_text(value, "context_id")

    @field_validator("roles")
    @classmethod
    def _valid_roles(cls, values: dict[str, list[str]]) -> dict[str, list[str]]:
        if not values:
            raise ValueError("RawFact roles must contain at least one role")
        cleaned: dict[str, list[str]] = {}
        for role, members in values.items():
            _require_text(role, "fact role")
            if not isinstance(members, list) or not members:
                raise ValueError(f"Fact role {role!r} must reference at least one mention")
            # Member order and multiplicity are part of the fact: two identical
            # participants are not the same assertion as one participant.
            cleaned[role] = [
                _require_text(member, "fact role member") for member in members
            ]
        return cleaned


class RawBatch(BaseModel):
    """One successfully transported extraction response for one chunk.

    ``complete`` and ``confirmed_empty`` both require an explicitly successful
    finish reason.  ``complete`` must contain at least one mention or fact;
    ``confirmed_empty`` must contain neither.  ``technical_failed`` keeps any
    partial payload for diagnosis but is never eligible for normal resolution.
    """

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    schema_version: str = SCHEMA_VERSION
    corpus_id: str
    doc_id: str
    revision_hash: str
    chunk_id: str
    chunk_hash: str
    raw_text: str
    extraction_id: str
    status: Literal["complete", "confirmed_empty", "technical_failed"]
    finish_reason: str
    prompt_hash: str
    model_profile_hash: str
    response_hash: str
    mentions: list[Mention] = Field(default_factory=list)
    facts: list[RawFact] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator(
        "corpus_id",
        "doc_id",
        "revision_hash",
        "chunk_id",
        "chunk_hash",
        "extraction_id",
        "prompt_hash",
        "model_profile_hash",
        "response_hash",
    )
    @classmethod
    def _non_empty(cls, value: str) -> str:
        return _require_text(value, "RawBatch field")

    @field_validator("schema_version")
    @classmethod
    def _schema_matches(cls, value: str) -> str:
        if value != SCHEMA_VERSION:
            raise ValueError(
                f"RawBatch schema_version must be {SCHEMA_VERSION!r}, got {value!r}"
            )
        return value

    @field_validator("raw_text")
    @classmethod
    def _raw_text_non_empty(cls, value: str) -> str:
        if not isinstance(value, str) or not value:
            raise ValueError("raw_text must be the complete non-empty source chunk")
        return value

    @model_validator(mode="after")
    def _validate_batch(self) -> "RawBatch":
        if hashlib.sha256(self.raw_text.encode("utf-8")).hexdigest() != self.chunk_hash:
            raise ValueError("chunk_hash does not match the original raw_text")

        normalized_finish = self.finish_reason.strip().lower()
        if self.status in {"complete", "confirmed_empty"}:
            if normalized_finish not in SUCCESS_FINISH_REASONS:
                raise ValueError(
                    "A successful batch requires an explicit successful finish_reason, "
                    f"got {self.finish_reason!r}"
                )
        if self.status == "complete" and not (self.mentions or self.facts):
            raise ValueError(
                "A complete batch must contain at least one mention or fact; "
                "use confirmed_empty for a verified empty extraction"
            )
        if self.status == "confirmed_empty" and (self.mentions or self.facts):
            raise ValueError("A confirmed_empty batch must not contain mentions or facts")

        mention_ids: set[str] = set()
        local_ids: set[str] = set()
        for mention in self.mentions:
            if mention.mention_id in mention_ids:
                raise ValueError(f"Duplicate mention_id {mention.mention_id!r} in batch")
            mention_ids.add(mention.mention_id)
            if mention.local_id in local_ids:
                raise ValueError(f"Duplicate mention local_id {mention.local_id!r} in batch")
            local_ids.add(mention.local_id)
            if (
                mention.doc_id != self.doc_id
                or mention.revision_hash != self.revision_hash
                or mention.chunk_id != self.chunk_id
            ):
                raise ValueError(
                    f"Mention {mention.mention_id!r} origin does not match its batch"
                )
            for span in mention.evidence:
                validate_evidence(span, self.raw_text, self.chunk_id)

        fact_ids: set[str] = set()
        for fact in self.facts:
            if fact.local_id in fact_ids:
                raise ValueError(f"Duplicate fact local_id {fact.local_id!r} in batch")
            fact_ids.add(fact.local_id)
            for role, members in fact.roles.items():
                missing = [member for member in members if member not in local_ids]
                if missing:
                    raise ValueError(
                        f"Fact {fact.local_id!r} role {role!r} references unknown "
                        f"local mention IDs: {missing}"
                    )
            for span in fact.evidence:
                validate_evidence(span, self.raw_text, self.chunk_id)

        # Fail fast if any payload cannot be fingerprinted deterministically.
        digest(self.model_dump(mode="json"))
        return self


# ---------------------------------------------------------------------------
# Canonical registry entity
# ---------------------------------------------------------------------------


class AliasSpec(BaseModel):
    """A normalized alias declaration with its scope and review status."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    text: str
    normalizer: NormalizerName = "common_name"
    scope: str | list[str] | dict[str, Any] | None = None
    guards: dict[str, Any] = Field(default_factory=dict)
    kind: str | None = None
    granularity: Granularity | None = None
    domain: str | None = None
    review_status: ReviewStatus = "reviewed"
    notes: str | None = None
    ambiguous: bool = False

    @field_validator("text")
    @classmethod
    def _text_non_empty(cls, value: str) -> str:
        return _require_text(value, "Alias text")

    @field_validator("kind", "domain")
    @classmethod
    def _optional_non_empty(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _require_text(value, "Alias field")

    @field_validator("scope")
    @classmethod
    def _valid_scope(
        cls, value: str | list[str] | dict[str, Any] | None
    ) -> str | list[str] | dict[str, Any] | None:
        if value is None:
            return None
        if isinstance(value, str):
            return _require_text(value, "alias scope")
        if isinstance(value, list):
            if not value:
                raise ValueError("alias scope list must not be empty")
            return _dedupe([_require_text(item, "alias scope item") for item in value])
        if isinstance(value, dict):
            if not value:
                raise ValueError("alias scope mapping must not be empty")
            return value
        raise ValueError("alias scope must be a string, list of strings or mapping")

    @model_validator(mode="after")
    def _suggestion_is_scoped(self) -> "AliasSpec":
        if self.review_status == "migration_suggestion" and self.scope is None:
            raise ValueError(
                "An unreviewed migration suggestion requires an explicit scope"
            )
        return self


class CanonicalEntity(BaseModel):
    """A versioned identity declared in YAML.

    Display names may change without changing ``canonical_id``.  Aliases are
    kept as :class:`AliasSpec` objects so a plain YAML string and an explicit
    scoped mapping end up in one comparable representation.
    """

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    canonical_id: str
    canonical_name: str
    kind: str
    granularity: Granularity = "concept"
    aliases: list[AliasSpec] = Field(default_factory=list)
    scoped_aliases: list[AliasSpec] = Field(default_factory=list)
    identity_guards: list[str] = Field(default_factory=list)
    variant_dimensions: list[str] = Field(default_factory=list)
    properties: dict[str, Any] = Field(default_factory=dict)
    merge_policy: Literal["append_evidence"] = "append_evidence"
    parent_id: str | None = None
    redirect_to: str | None = None
    name_normalizer: NormalizerName | None = None
    status: Literal["confirmed", "provisional", "retired"] = "confirmed"
    notes: str | None = None

    @field_validator("canonical_id", "canonical_name", "kind")
    @classmethod
    def _non_empty(cls, value: str) -> str:
        return _require_text(value, "CanonicalEntity field")

    @field_validator("identity_guards", "variant_dimensions")
    @classmethod
    def _valid_dimension_names(cls, values: list[str]) -> list[str]:
        return _dedupe([_require_text(value, "guard dimension") for value in values])

    @field_validator("aliases", "scoped_aliases", mode="before")
    @classmethod
    def _coerce_aliases(cls, values: Any) -> Any:
        if values is None:
            return []
        if isinstance(values, (str, Mapping, AliasSpec)):
            values = [values]
        if not isinstance(values, list):
            raise ValueError("aliases must be a string, mapping or list")
        prepared: list[Any] = []
        for item in values:
            if isinstance(item, AliasSpec):
                prepared.append(item)
            elif isinstance(item, str):
                prepared.append({"text": item})
            elif isinstance(item, Mapping):
                prepared.append(dict(item))
            else:
                raise ValueError("Each alias must be a string or mapping")
        return prepared

    @model_validator(mode="after")
    def _validate_entity(self) -> "CanonicalEntity":
        if self.redirect_to is not None:
            _require_text(self.redirect_to, "redirect_to")
            if self.redirect_to == self.canonical_id:
                raise ValueError("An entity cannot redirect to itself")
        if self.parent_id is not None:
            _require_text(self.parent_id, "parent_id")
            if self.parent_id == self.canonical_id:
                raise ValueError("An entity cannot be its own parent")
        for alias in self.scoped_aliases:
            if alias.scope is None:
                raise ValueError(
                    f"Scoped alias {alias.text!r} on {self.canonical_id!r} has no scope"
                )
        return self


# ---------------------------------------------------------------------------
# Configuration guards
# ---------------------------------------------------------------------------


def _resolve_path(path: str | os.PathLike[str]) -> Path:
    return Path(path).expanduser().resolve()


def _normcase(path: Path) -> str:
    return os.path.normcase(os.path.abspath(str(path)))


def _same_path(left: Path, right: Path) -> bool:
    return _normcase(left) == _normcase(right)


def _is_within(child: Path, parent: Path) -> bool:
    child_key = _normcase(child)
    parent_key = _normcase(parent)
    if child_key == parent_key:
        return True
    try:
        return os.path.commonpath([child_key, parent_key]) == parent_key
    except ValueError:  # Different drives on Windows.
        return False


def _published_reason(target: Path) -> str | None:
    for marker in PUBLISHED_MARKERS:
        if (target / marker).exists():
            return f"target contains published marker {marker!r}"
    manifest = target / "run_manifest.json"
    if manifest.is_file():
        try:
            payload = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            return f"target has an unreadable run_manifest.json: {exc}"
        if isinstance(payload, dict):
            status = str(payload.get("status") or payload.get("publication_status") or "").lower()
            if status in PUBLISHED_MANIFEST_STATUSES:
                return f"target manifest reports status {status!r}"
    return None


def validate_source_target(
    source: str | os.PathLike[str],
    target: str | os.PathLike[str],
    *,
    accepted_targets: Iterable[str | os.PathLike[str]] = (),
) -> tuple[str, str]:
    """Reject source/target layouts that could mutate sources or accepted data.

    Rules:

    * source and target must be different;
    * neither may contain the other;
    * target must not be an accepted/published target (explicitly supplied or
      marked by a published manifest/marker);
    * target cannot be an ordinary file.

    The return value is ``(resolved_source, resolved_target)`` for logging.
    """

    source_path = _resolve_path(source)
    target_path = _resolve_path(target)

    if _same_path(source_path, target_path):
        raise ValueError("Normalization source and target must be different paths")
    if _is_within(target_path, source_path):
        raise ValueError("Normalization target must not be inside the source tree")
    if _is_within(source_path, target_path):
        raise ValueError("Normalization source must not be inside the target tree")
    if target_path.exists() and target_path.is_file():
        raise ValueError("Normalization target must be a directory, not a file")

    for accepted in accepted_targets:
        accepted_path = _resolve_path(accepted)
        if _is_within(target_path, accepted_path) or _is_within(accepted_path, target_path):
            raise ValueError(
                f"Normalization target overlaps accepted/published target {accepted_path}"
            )

    for candidate in (target_path, *target_path.parents):
        reason = _published_reason(candidate)
        if reason:
            raise ValueError(f"Refusing to write into accepted output: {reason}")

    return str(source_path), str(target_path)


def validate_strategy_config(config: Mapping[str, Any] | None) -> dict[str, Any]:
    """Validate strategy routing fields and return a frozen summary.

    A configuration without ``normalization_strategy`` keeps legacy semantics;
    it is never inferred to be v2.  An explicit v2 configuration is required to
    be offline and to use the fixed candidate cap and EFU-disabled controls.
    """

    if config is None:
        config = {}
    if not isinstance(config, Mapping):
        raise ValueError("normalization strategy configuration must be a mapping")

    cfg = dict(config)
    raw_strategy = cfg.get("normalization_strategy")
    if raw_strategy in (None, ""):
        # Legacy configuration: preserve existing semantics exactly.  Do not
        # add v2 defaults or reinterpret the old enable flag.
        return {
            "strategy": None,
            "legacy": True,
            "normalization_phase": cfg.get("normalization_phase"),
            "normalize_during_extraction": bool(
                cfg.get(
                    "normalize_during_extraction",
                    cfg.get("enable_entity_normalization", False),
                )
            ),
            "candidate_cap": cfg.get("candidate_cap"),
            "efu_repair": cfg.get("efu_repair", cfg.get("enable_efu")),
        }

    if not isinstance(raw_strategy, str):
        raise ValueError("normalization_strategy must be a string")
    strategy = raw_strategy.strip()
    if strategy in LEGACY_STRATEGIES:
        if strategy == "legacy_posthoc" and cfg.get("normalize_during_extraction") is True:
            raise ValueError("legacy_posthoc cannot normalize during extraction")
        return {
            "strategy": strategy,
            "legacy": True,
            "normalization_phase": cfg.get("normalization_phase"),
            "normalize_during_extraction": bool(
                cfg.get("normalize_during_extraction", False)
            ),
            "candidate_cap": cfg.get("candidate_cap"),
            "efu_repair": cfg.get("efu_repair", cfg.get("enable_efu")),
        }
    if strategy != STRATEGY:
        raise ValueError(
            f"Unknown normalization_strategy {strategy!r}; expected {STRATEGY!r} "
            "or an explicit legacy strategy"
        )

    normalize_during = cfg.get("normalize_during_extraction")
    if normalize_during is True:
        raise ValueError(
            "registry_offline_v2 requires normalize_during_extraction=false; "
            "contradictory online normalization is not allowed"
        )
    legacy_enable = cfg.get("enable_entity_normalization")
    if legacy_enable is True and normalize_during is not False:
        raise ValueError(
            "registry_offline_v2 cannot enable the legacy extraction-time hook; "
            "set normalize_during_extraction=false explicitly"
        )

    phase = cfg.get("normalization_phase", "posthoc")
    if not isinstance(phase, str) or not phase.strip():
        raise ValueError("normalization_phase must be a non-empty string")
    phase_value = phase.strip().lower()
    if phase_value in ONLINE_PHASES:
        raise ValueError("registry_offline_v2 cannot run during extraction")
    if phase_value not in OFFLINE_PHASES:
        raise ValueError(
            f"Unsupported offline normalization_phase {phase!r}; "
            f"expected one of {sorted(OFFLINE_PHASES)}"
        )

    candidate_cap = cfg.get("candidate_cap", 5)
    if candidate_cap != 5:
        raise ValueError("registry_offline_v2 fixes candidate_cap at 5")

    for flag in ("efu_repair", "enable_efu", "efu"):
        if cfg.get(flag) is True:
            raise ValueError("registry_offline_v2 requires EFU repair to be false")

    embedding_calls = cfg.get("identity_candidate_embedding_calls", 0)
    if embedding_calls not in (0, None):
        raise ValueError(
            "registry_offline_v2 does not use identity-candidate embeddings"
        )

    if cfg.get("default_strategy_auto_switch") is True:
        raise ValueError("registry_offline_v2 cannot silently become the default strategy")

    return {
        "strategy": STRATEGY,
        "legacy": False,
        "normalization_phase": phase_value,
        "normalize_during_extraction": False,
        "candidate_cap": 5,
        "efu_repair": False,
        "identity_candidate_embedding_calls": 0,
        "legacy_online_hook": False,
    }
