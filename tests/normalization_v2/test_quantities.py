from decimal import Decimal

import pytest

from hyperche.normalization_v2.quantities import UnitRegistry, decimal_text, number, observation


def obs(value=None, unit=None, **extra):
    args = {"metric_id": "metric:pfoa_defluorination", "roles": {"target": ["pfas:pfoa"]},
            "doc_id": "doc1", "revision_hash": "revision1", "chunk_id": "chunk1",
            "local_id": "measurement1", "context_id": "experiment1"}
    quantity = {"value": value, "unit": unit}
    for key in list(extra):
        if key in args:
            args[key] = extra.pop(key)
    quantity.update(extra)
    return observation(quantity, **args)


def test_units_convert_deterministically_and_preserve_original_values():
    a, b = obs("95", "%"), obs("0.95", "1")
    assert a["canonical"]["value"] == b["canonical"]["value"] == "0.95"
    assert a["raw"]["value"] == "95"
    assert obs("1000", "ug/L")["canonical"]["value"] == obs("1", "mg/L")["canonical"]["value"]
    assert obs("1", "mg/L")["canonical"]["value"] != obs("1", "ug/L")["canonical"]["value"]
    assert obs("1", "mM")["canonical"]["value"] != obs("1", "M")["canonical"]["value"]


def test_experiment_role_and_metric_scopes_never_collapse():
    a = obs(95, "%")
    assert a["observation_id"] != obs(95, "%", context_id="experiment2")["observation_id"]
    assert a["observation_id"] != obs(95, "%", doc_id="doc2")["observation_id"]
    assert a["observation_id"] != obs(95, "%", metric_id="metric:pfoa_removal")["observation_id"]
    assert a["observation_id"] != obs(95, "%", roles={"target": ["pfas:pfos"]})["observation_id"]


@pytest.mark.parametrize("value", [True, False, float("nan"), float("inf"), "not a number"])
def test_invalid_numbers_preserved_with_failure_status(value):
    row = obs(value, "%")
    assert row["status"] == "preserved_unresolved"
    assert row["canonical"] is None
    assert row["reason"]


def test_no_description_or_formula_digit_inference():
    assert obs(None, "%", description="90% at 60 min")["canonical"] is None
    assert obs(None, "mM", raw_name="Na2SO4")["canonical"] is None
    assert obs(90, None)["canonical"] is None
    assert obs(90, "unknown unit")["canonical"] is None


def test_ranges_and_temperature_semantics():
    row = obs(None, "min", value_min="1", value_max="2")
    assert row["canonical"]["value_min"] == "60"
    assert row["canonical"]["value_max"] == "120"
    assert obs(1, "min", value_min=1, value_max=2)["canonical"] is None
    assert obs(None, "min", value_min=2, value_max=1)["canonical"] is None
    assert obs(None, "min", value_min=1)["canonical"] is None
    assert obs(25, "C")["canonical"] is None
    assert obs(25, "C", temperature_kind="absolute")["canonical"]["value"] == "298.15"
    assert obs(25, "C", temperature_kind="difference")["canonical"]["value"] == "25"


def test_unit_collision_dimension_guards_and_decimal_precision():
    with pytest.raises(ValueError, match="Conflicting"):
        UnitRegistry([{"symbol": "a", "aliases": ["same"], "dimension": "x", "base_unit": "x", "scale": "1"},
                      {"symbol": "b", "aliases": ["same"], "dimension": "x", "base_unit": "x", "scale": "2"}])
    with pytest.raises(ValueError, match="dimension"):
        UnitRegistry().convert(Decimal("1"), "mg/L", dimension="voltage")
    assert decimal_text(number("1.2000e-4")) == "0.00012"
    assert decimal_text(number("-0.0")) == "0"
    assert obs("9.5e1", "%")["canonical"]["value"] == "0.95"
