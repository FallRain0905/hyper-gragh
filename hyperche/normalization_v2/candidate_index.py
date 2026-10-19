"""Bounded, lexical candidate retrieval. A match here never proves identity.

No embedding client, pair expansion, or shared-component material bucket is
used. Posting lists are visited only for the current mention. Broad ambiguity
is reported without quietly truncating it into an apparently complete task.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Mapping

from .contracts import CanonicalEntity, Mention
from .text_policy import default_normalizer_for_kind, fuzzy_key, normalize


@dataclass(frozen=True)
class CandidateResult:
    candidates: tuple[CanonicalEntity, ...]
    too_broad: bool
    matched_count: int
    reasons: dict[str, tuple[str, ...]]


def compatible(mention: Mention, entity: CanonicalEntity, *, exact=False) -> bool:
    if entity.status == "retired" or entity.kind != mention.kind:
        return False
    if entity.granularity != mention.granularity:
        return False
    for field in set(entity.identity_guards) | set(entity.variant_dimensions):
        left, right = mention.attributes.get(field), entity.properties.get(field)
        if left is not None and right is not None and left != right:
            return False
        if exact and field in entity.identity_guards and (left is None or right is None):
            return False
        if exact and field in entity.variant_dimensions and left is not None and right is None:
            return False
    return True


class CandidateIndex:
    def __init__(self, entities: Iterable[CanonicalEntity | Mapping] = (), *, limit=5):
        if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 5:
            raise ValueError("candidate limit must be between 1 and 5")
        self.limit = limit
        self.entities: dict[str, CanonicalEntity] = {}
        self.postings: dict[tuple[str, str, str], set[str]] = defaultdict(set)
        for entity in entities:
            self.add(entity)

    def add(self, entity: CanonicalEntity | Mapping):
        entity = CanonicalEntity.model_validate(entity)
        self.entities[entity.canonical_id] = entity
        names = [(entity.canonical_name, entity.name_normalizer or default_normalizer_for_kind(entity.kind))]
        names += [(a.text, a.normalizer) for a in [*entity.aliases, *entity.scoped_aliases]]
        for name, policy in names:
            for key in (normalize(name, policy), fuzzy_key(name, policy)):
                self.postings[(entity.kind, entity.granularity, key)].add(entity.canonical_id)

    def find(self, mention: Mention | Mapping, *, exclude=()) -> CandidateResult:
        mention = Mention.model_validate(mention)
        found: dict[str, set[str]] = defaultdict(set)
        excluded = set(exclude)
        # Explicit model alias strings are retrieval clues, never trusted keys.
        for name in [mention.raw_name, *mention.aliases]:
            for policy in ("chemical_formula", "common_name", "exact"):
                for key in (normalize(name, policy), fuzzy_key(name, policy)):
                    for identifier in self.postings.get((mention.kind, mention.granularity, key), ()):
                        entity = self.entities[identifier]
                        if identifier not in excluded and compatible(mention, entity):
                            found[identifier].add("lexical:" + policy)
        count = len(found)
        broad = count > self.limit
        identifiers = [] if broad else sorted(found)
        return CandidateResult(tuple(self.entities[i] for i in identifiers), broad, count,
                               {i: tuple(sorted(found[i])) for i in identifiers})
