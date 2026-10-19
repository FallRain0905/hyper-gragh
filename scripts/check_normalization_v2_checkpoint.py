"""Recompute source/preservation checks for this development checkpoint only."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from hyperche.normalization_v2.contracts import digest
from hyperche.normalization_v2.registry import Registry


def sha(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""): value.update(block)
    return value.hexdigest()


def main():
    doc = ROOT / "docs/normalization_v2"
    baseline = json.loads((doc / "baseline.json").read_text(encoding="utf-8"))
    protected = baseline["protected_source_files"]
    changes = []
    for record in protected:
        path = ROOT / record["path"]
        if not path.is_file() or sha(path) != record["worktree_sha256"]:
            changes.append(record["path"])
    intentional = {"web-ui/backend/runtime_requests.py"}
    unexpected = sorted(set(changes) - intentional)
    sources = [*sorted((ROOT / "hyperche/normalization_v2").glob("*.py")),
               ROOT / "hyperche/request_leases.py", ROOT / "web-ui/backend/runtime_requests.py",
               *sorted((ROOT / "tests/normalization_v2").glob("*.py")),
               *sorted((ROOT / "configs/normalization_v2").glob("*.yaml")),
               *[ROOT / "scripts" / name for name in ("normalize_registry_offline.py", "run_zcode_delegate.py", "audit_normalization_v2_migration.py", "curate_normalization_v2_seed.py", "check_normalization_v2_checkpoint.py")]]
    syntax, sensitive = [], []
    for path in sources:
        content = path.read_text(encoding="utf-8")
        if path.suffix == ".py":
            try: compile(content, str(path), "exec")
            except SyntaxError: syntax.append(str(path.relative_to(ROOT)))
        if re.search(r"\b(?:sk|gsk|rk|xai)[-_][A-Za-z0-9_-]{16,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", content):
            sensitive.append(str(path.relative_to(ROOT)))
    preservation_file = Path(r"D:\Hyper-rag-case2-backups\case2_case1_aligned_v1\preservation_before.json")
    preservation = {"status": "unavailable", "checked": 0, "mismatches": [], "scope": "Historical case2 accepted build/published files and original gold/QA records selected from the pre-alignment manifest"}
    if preservation_file.exists():
        inventory = json.loads(preservation_file.read_text(encoding="utf-8"))
        for name, expected in inventory.items():
            normalized = name.replace("\\", "/").lower()
            if not any(s in normalized for s in ("case2_pfas_build/hyper_", "web-ui/backend/hyperrag_cache/case2/", "gold_v2/qa_gold.json", "evaluation_v2/records/")):
                continue
            path = Path(name)
            preservation["checked"] += 1
            if not path.is_file() or sha(path) != expected:
                preservation["mismatches"].append(name)
        preservation["status"] = "passed" if preservation["checked"] and not preservation["mismatches"] else "failed"
        preservation["inventory_sha256"] = sha(preservation_file)
    registry = Registry.from_paths(ROOT / "configs/normalization_v2")
    hashes = {str(path.relative_to(ROOT)).replace("\\", "/"): sha(path) for path in sources}
    report = {"checked_at": datetime.now(timezone.utc).isoformat(), "status": "development_checkpoint_not_release",
        "strategy": "registry_offline_v2", "full_v2_accepted": False, "default_strategy_changed": False,
        "legacy_baseline": {"commit": baseline["legacy_commit"], "tag": baseline["legacy_tag"],
            "checked_sources": len(protected), "intentional_runtime_changes": sorted(set(changes) & intentional), "unexpected_changes": unexpected},
        "source_screen": {"files": len(sources), "syntax_errors": syntax, "sensitive_pattern_hits": sensitive,
            "limitation": "Pattern screening is not a formal secret or repository-history audit."},
        "source_hashes": hashes, "source_tree_hash": digest(hashes),
        "registry": {"entities": len(registry.entities), "units": len(registry.units), "semantic_hash": registry.snapshot_hash,
                     "annotation_status": "machine_curated_not_independent_human_gold"},
        "selected_test_evidence": "test_result_20261019.json", "case2_preservation": preservation,
        "release_gates": {f"G{i:02}": "insufficient_evidence_for_full_gate" for i in range(1, 15)},
        "limitations": ["Full builder/Web/legacy-import and command-family integration remains incomplete.",
            "All legacy API callers and hidden SDK retries are not yet integrated with the broker.",
            "No new real-corpus identity-quality or total-cost experiment was run.",
            "ZCODE coding requests do not count as normalization or scientific-quality evidence."]}
    (doc / "implementation_checks.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"syntax_errors": syntax, "sensitive_pattern_hits": sensitive,
                      "unexpected_legacy_changes": unexpected,
                      "case2_checked": preservation["checked"], "case2_mismatches": len(preservation["mismatches"])}))
    return 1 if unexpected or syntax or sensitive or preservation["mismatches"] else 0


if __name__ == "__main__": raise SystemExit(main())
