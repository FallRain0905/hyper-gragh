"""Dictionary-first, offline identity normalization (registry_offline_v2).

The package deliberately separates three concerns:

* :mod:`hyperche.normalization_v2.contracts` -- versioned extraction and
  evidence records, deterministic fingerprints and configuration guards;
* :mod:`hyperche.normalization_v2.text_policy` -- safe surface-form keys that
  keep chemical case, charge and valence distinctions;
* :mod:`hyperche.normalization_v2.registry` -- the declarative YAML compiler,
  scoped exact lookup index and dependency-scoped hashes.

Importing the package starts no jobs and makes no model calls. Explicit
offline adapters and judgment workers are separate modules; legacy extraction
hooks and defaults are not enabled by importing this namespace.
"""

from .contracts import (
    LEGACY_STRATEGIES,
    SCHEMA_VERSION,
    STRATEGY,
    CanonicalEntity,
    EvidenceSpan,
    Mention,
    RawBatch,
    RawFact,
    canonical_json,
    digest,
    locate_evidence,
    stable_id,
    utc_now,
    validate_evidence,
    validate_source_target,
    validate_strategy_config,
)
from .registry import (
    AliasBinding,
    HighRiskGroup,
    NegativePair,
    Registry,
    RegistryError,
    RoleDefinition,
    UnitDefinition,
)
from .text_policy import (
    POLICIES,
    default_normalizer_for_kind,
    fuzzy_key,
    normalize,
)

__all__ = [
    "AliasBinding",
    "CanonicalEntity",
    "EvidenceSpan",
    "HighRiskGroup",
    "LEGACY_STRATEGIES",
    "Mention",
    "NegativePair",
    "POLICIES",
    "RawBatch",
    "RawFact",
    "Registry",
    "RegistryError",
    "RoleDefinition",
    "SCHEMA_VERSION",
    "STRATEGY",
    "UnitDefinition",
    "canonical_json",
    "default_normalizer_for_kind",
    "digest",
    "fuzzy_key",
    "locate_evidence",
    "normalize",
    "stable_id",
    "utc_now",
    "validate_evidence",
    "validate_source_target",
    "validate_strategy_config",
]
