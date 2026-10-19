from hyperche.normalization_v2.text_policy import normalize, fuzzy_key


def test_chemical_scripts_case_and_charge_remain_distinct():
    assert normalize("H₂SO₄", "chemical_formula") == normalize("H2SO4", "chemical_formula")
    assert normalize("VO²⁺", "chemical_formula") == normalize("VO^2+", "chemical_formula")
    assert normalize("VO²⁺", "chemical_formula") != normalize("VO₂⁺", "chemical_formula")
    assert normalize("Co", "chemical_formula") != normalize("CO", "chemical_formula")
    assert normalize("TiO2", "chemical_formula") != normalize("TiO2/PVDF", "chemical_formula")


def test_fuzzy_lookup_keys_are_separate_from_identity_keys():
    assert normalize("iron-chromium", "common_name") == normalize("Iron chromium", "common_name")
    assert fuzzy_key("PFOA-7", "chemical_formula") == fuzzy_key("PFOA7", "chemical_formula")
    assert fuzzy_key("PFOA-7", "chemical_formula") != normalize("PFOA7", "chemical_formula")
