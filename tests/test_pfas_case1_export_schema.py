from scripts.finalize_pfas_case1_schema import source_summary


def test_source_hit_must_use_retrieved_chunk_grade_not_other_chunk_in_paper():
    ranks = {("F1", "Q"): [(1, "PFAS_001_CHK_001")]}
    grades = {("Q", "PFAS_001_CHK_001"):0, ("Q", "PFAS_001_CHK_002"):3}
    rows = source_summary(["F1"], ["Q"], ranks, grades)
    assert all(r["Source-level Hit@5"] == r["chunk Hit@5 (same qrel policy)"] == 0 for r in rows)
    grades["Q", "PFAS_001_CHK_001"] = 2
    rows = source_summary(["F1"], ["Q"], ranks, grades)
    assert rows[0]["Source-level Hit@5"] == 1 and rows[1]["Source-level Hit@5"] == 0
