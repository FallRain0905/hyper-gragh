"""Apply explicit conservative corrections to the unreleased machine seed.

This is a development migration, never a runtime auto-learning operation.
Run only against the new configs/normalization_v2 namespace. The disposition
report records the rejected equivalences rather than silently inheriting them.
"""
from pathlib import Path
import json
import yaml


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configs/normalization_v2"


def main():
    corrections = []
    removals = {
        "evidence:lc_ms_ms": {"tandem mass spectrometry": "Tandem MS alone does not specify LC coupling."},
        "evidence:fluoride_release": {"fluoride yield": "A quantitative yield and evidence of release are related, not identical."},
        "system:organic_redox_flow_battery": {"aqueous organic redox flow battery": "Aqueous is a material system restriction."},
        "electrode:activated_carbon_felt": {"activated graphite felt": "Graphite and carbon felt are distinct substrates.",
                                            "thermally activated carbon felt": "Activation method is a variant, not a universal equivalence."},
        "metric:ohmic_resistance": {"ohmic loss": "Resistance and a voltage/energy loss have different quantities."},
        "degradation:dendrite_growth": {"zinc dendrite growth": "Specific element cannot be erased."},
        "condition:acid_concentration": {"H2SO4 concentration": "Generic acid concentration does not establish sulfuric acid.",
                                          "sulfuric acid concentration": "Generic acid concentration does not establish sulfuric acid."},
        "species:pb2_plus": {"lead ion": "Unspecified oxidation state is not necessarily Pb(II).", "lead ions": "Oxidation state is unspecified."},
        "species:bi3_plus": {"bismuth ion": "Unspecified oxidation state is not necessarily Bi(III)."},
        "pfas:ptfe": {"Teflon": "Brand name may denote distinct fluoropolymers."},
        "material:bi4ti3o12": {"bismuth titanate": "Bismuth titanates include multiple stoichiometries."},
        "metric:degradation_efficiency": {"removal efficiency": "Removal does not imply chemical degradation.",
                                           "degradation rate": "Kinetic rate and endpoint fraction are distinct."},
        "metric:defluorination_efficiency": {"defluorination rate": "Kinetic rate and endpoint fraction are distinct."},
        "metric:mineralization_efficiency": {"mineralization rate": "Kinetic rate and endpoint fraction are distinct."},
    }
    kind_mapping = {"contaminant": "chemical", "membrane": "material", "electrode": "material",
                    "catalyst": "material", "polymer": "material", "condition": "metric",
                    "property": "metric", "degradation": "process", "water_matrix": "mixture"}
    for path in sorted(CONFIG.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or "entities" not in data: continue
        if data.get("defaults", {}).get("seed_curation_version") == "conservative-1": continue
        data.setdefault("defaults", {})["seed_curation_version"] = "conservative-1"
        domain = data["domain"]
        entities = data["entities"]
        by_id = {e["canonical_id"]: e for e in entities}
        for entity in entities:
            identifier = entity["canonical_id"]
            original_kind = entity["kind"]
            entity["kind"] = kind_mapping.get(original_kind, original_kind)
            # Roles must be supplied in facts, not used as substance identity.
            if original_kind != entity["kind"]:
                corrections.append({"id": identifier, "change": "object_kind", "from": original_kind, "to": entity["kind"]})
            for field, reason in removals.get(identifier, {}).items():
                old = entity.get("aliases", [])
                if any((a if isinstance(a, str) else a["text"]) == field for a in old):
                    entity["aliases"] = [a for a in old if (a if isinstance(a, str) else a["text"]) != field]
                    entity.setdefault("scoped_aliases", []).append({"text": field, "normalizer": "common_name",
                        "scope": {"domain": domain}, "review_status": "migration_suggestion", "notes": reason})
                    corrections.append({"id": identifier, "alias": field, "disposition": "candidate_only", "reason": reason})
            # Explicit conflicting attributes cannot bind a generic concept.
            if entity["kind"] in {"material", "chemical", "species"}:
                entity["variant_dimensions"] = sorted(set(entity.get("variant_dimensions", [])) |
                    {"phase", "charge", "oxidation_state", "protonation", "counterion", "membrane_model", "composition", "sample_id"})
            if original_kind == "sample":
                entity["status"] = "retired"
                entity["notes"] = "Unscoped sample labels are never globally resolved; use source-local provisional identities."
        if domain == "pfas":
            for abbreviation in ("pfoa", "pfos", "pfba", "pfbs"):
                generic, acid = by_id["pfas:" + abbreviation], by_id["pfas:" + abbreviation + "_acid"]
                data.get("redirects", {}).pop(acid["canonical_id"], None)
                acid.pop("redirect_to", None)
                acid.update(canonical_name=next(a for a in generic["aliases"] if isinstance(a, str)),
                            aliases=generic.get("aliases", []), properties=dict(generic.get("properties", {})),
                            parent_id=generic["canonical_id"])
                generic["aliases"] = []
                generic.get("properties", {}).pop("protonation", None)
                generic.setdefault("properties", {})["form"] = "unspecified"
                corrections.append({"id": generic["canonical_id"], "change": "bare_abbreviation_form_unspecified",
                                    "acid_id": acid["canonical_id"], "reason": "Bare abbreviation alone does not prove protonation."})
            additions = [
                {"canonical_id": "metric:removal_efficiency", "canonical_name": "removal efficiency", "kind": "metric", "aliases": ["removal fraction", "removal percentage"]},
                {"canonical_id": "metric:degradation_rate", "canonical_name": "degradation rate", "kind": "metric"},
                {"canonical_id": "metric:defluorination_rate", "canonical_name": "defluorination rate", "kind": "metric"},
                {"canonical_id": "metric:mineralization_rate", "canonical_name": "mineralization rate", "kind": "metric"},
            ]
            entities.extend(e for e in additions if e["canonical_id"] not in by_id)
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
    target = ROOT / "docs/normalization_v2/seed_curation.json"
    if corrections or not target.exists():
        target.write_text(json.dumps({"status": "machine_curated_not_independent_human_gold",
                                  "changes": corrections}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
