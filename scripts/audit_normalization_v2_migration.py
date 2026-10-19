"""Inventory every legacy name against the unreleased v2 seed, without merging."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from hyperche.normalization_v2.registry import Registry
from hyperche.normalization_v2.text_policy import normalize


def build():
    registry = Registry.from_paths(ROOT / "configs/normalization_v2")
    records, sources = [], {}
    for relative in ("configs/normalization/alias_registry.yaml", "configs/normalization/pfas.yaml"):
        path = ROOT / relative
        sources[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        for old in payload.get("entities", payload.get("canonical_entities", [])):
            canonical_matches = {e.canonical_id for kind in {e.kind for e in registry.entities.values()}
                for granularity in ("concept", "variant", "sample")
                for e in registry.lookup(old["canonical_name"], kind, granularity=granularity)}
            for name in dict.fromkeys([old["canonical_name"], *old.get("aliases", [])]):
                matches = {e.canonical_id for kind in {e.kind for e in registry.entities.values()}
                    for granularity in ("concept", "variant", "sample")
                    for e in registry.lookup(name, kind, granularity=granularity)}
                suggestions = sorted({a.entity_id for a in registry.suggestions
                                      if normalize(name, a.normalizer) == a.normalized})
                if not matches:
                    disposition = "candidate_only" if suggestions else "not_in_trusted_seed"
                    reason = "No unconditional equivalence is inherited; retain local provisional identity or review the explicit scoped candidate."
                elif canonical_matches and matches != canonical_matches:
                    disposition = "identity_split"
                    reason = "V2 maps this surface to a distinct identity; legacy equivalence is not inherited."
                else:
                    disposition = "seed_equivalence"
                    reason = "Available as a deterministic seed mapping; independent scientific review is not implied."
                records.append({"source": relative, "old_id": old["canonical_id"],
                    "old_name": old["canonical_name"], "surface": name, "new_ids": sorted(matches),
                    "candidate_ids": suggestions, "disposition": disposition, "reason": reason})
    return {"status": "machine_migration_inventory_not_human_gold", "registry_hash": registry.snapshot_hash,
            "source_sha256": sources, "counts": dict(Counter(r["disposition"] for r in records)),
            "records": records}


if __name__ == "__main__":
    target = ROOT / "docs/normalization_v2/migration_dispositions.json"
    target.write_text(json.dumps(build(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
