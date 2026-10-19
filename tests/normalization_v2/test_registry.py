import copy
from decimal import Decimal
from pathlib import Path

import pytest

from hyperche.normalization_v2.contracts import AliasSpec, CanonicalEntity
from hyperche.normalization_v2.quantities import UnitRegistry
from hyperche.normalization_v2.registry import Registry, RegistryError


CONFIG = Path(__file__).resolve().parents[2] / "configs/normalization_v2"


def entity(eid, name, **kw):
    return CanonicalEntity(canonical_id=eid, canonical_name=name, kind="material", **kw)


def ids(registry, name, kind, **kwargs):
    return [e.canonical_id for e in registry.lookup(name, kind, **kwargs)]


def test_real_domain_registries_compile_together_deterministically():
    first, second = Registry.from_paths(CONFIG), Registry.from_paths(list(reversed(sorted(CONFIG.glob("*.yaml")))))
    assert first.snapshot_hash == second.snapshot_hash
    assert len(first.entities) >= 100 and len(first.units) >= 30
    assert ids(first, "Co", "species") == ["species:cobalt"]
    assert ids(first, "CO", "species") == ["species:carbon_monoxide"]
    assert ids(first, "VO²⁺", "species") == ["species:vanadyl_ion"]
    assert ids(first, "VO₂⁺", "species") == ["species:dioxovanadium_v"]
    assert ids(first, "LC-MS", "evidence") != ids(first, "LC-MS/MS", "evidence")
    assert ids(first, "PFOA", "chemical") != ids(first, "perfluorooctanoic acid", "chemical")
    assert ids(first, "perfluorooctanoate", "chemical") != ids(first, "perfluorooctanoic acid", "chemical")
    assert ids(first, "removal efficiency", "metric") != ids(first, "degradation efficiency", "metric")
    assert ids(first, "degradation rate", "metric") != ids(first, "degradation efficiency", "metric")
    assert ids(first, "defluorination efficiency", "metric") != ids(first, "mineralization efficiency", "metric")


def test_compiled_export_round_trip_keeps_semantic_hash(tmp_path):
    registry = Registry.from_paths(CONFIG)
    target = tmp_path / "snapshot.yaml"
    assert registry.export(target) == registry.snapshot_hash
    assert Registry.from_paths(target).snapshot_hash == registry.snapshot_hash
    with pytest.raises(RegistryError, match="exists"): registry.export(target)


def test_specific_variants_do_not_bind_generic_or_conflicting_models():
    registry = Registry.from_paths(CONFIG)
    assert ids(registry, "Nafion117", "material", granularity="variant") == ["membrane:nafion_117"]
    assert not ids(registry, "Nafion117", "material", granularity="variant", attributes={"membrane_model": "115"})
    assert not ids(registry, "Nafion", "material", attributes={"membrane_model": "117"})
    assert not ids(registry, "TiO2", "material", attributes={"phase": "anatase"})
    assert ids(registry, "anatase TiO2", "material", granularity="variant", attributes={"phase": "anatase"}) == ["material:tio2_anatase"]
    assert not ids(registry, "Sample A", "sample")
    assert not ids(registry, "Teflon", "material")


def test_scoped_alias_guards_are_compared_as_typed_values():
    registry = Registry([entity("one", "model-one", scoped_aliases=[AliasSpec(text="M", normalizer="exact", scope={"doc_id": "d1"}, guards={"model": "117"})]),
                         entity("two", "model-two", scoped_aliases=[AliasSpec(text="M", normalizer="exact", scope={"doc_id": "d2"})])])
    assert ids(registry, "M", "material", scope={"doc_id": "d1"}, attributes={"model": "117"}) == ["one"]
    assert not ids(registry, "M", "material", scope={"doc_id": "d1"})
    assert not ids(registry, "M", "material", scope={"doc_id": "d3"})
    assert ids(registry, "M", "material", scope={"doc_id": "d2"}) == ["two"]


def test_intentional_ambiguity_requires_explicit_declaration():
    def entries(ambiguous):
        return [entity(str(i), "canonical" + str(i), scoped_aliases=[AliasSpec(text="X", scope={"domain": "pfas"}, ambiguous=ambiguous)]) for i in (1, 2)]
    with pytest.raises(RegistryError, match="Overlapping"): Registry(entries(False))
    registry = Registry(entries(True))
    assert ids(registry, "X", "material", scope={"domain": "pfas"}) == ["1", "2"]
    with pytest.raises(RegistryError, match="unscoped"):
        Registry([entity("1", "name", aliases=["x"]), entity("2", "another", aliases=["x"])])


def test_unreviewed_and_migration_candidates_are_not_trusted_dictionary_keys():
    registry = Registry([entity("one", "one", aliases=[AliasSpec(text="unchecked", review_status="unreviewed")],
                               scoped_aliases=[AliasSpec(text="maybe", scope={"doc_id": "d"}, review_status="migration_suggestion")])])
    assert not ids(registry, "unchecked", "material")
    assert not ids(registry, "maybe", "material", scope={"doc_id": "d"})
    assert ids(registry, "unchecked", "material", include_unreviewed=True) == ["one"]


def test_related_dependencies_change_but_unrelated_names_do_not():
    one = entity("one", "one")
    first = Registry([one])
    second = Registry([one, entity("unrelated", "other")])
    assert first.dependency_hash(["one"]) == second.dependency_hash(["one"])
    modified = one.model_copy(update={"aliases": [AliasSpec(text="new alias")]})
    assert Registry([modified]).dependency_hash(["one"]) != first.dependency_hash(["one"])


def test_units_have_explicit_bases_and_preserve_prefix_case_and_temperature_meaning():
    registry = Registry.from_paths(CONFIG)
    units = UnitRegistry.from_compiled(registry)
    assert units.convert(Decimal("1"), "mM")[0] == Decimal("0.001")
    assert units.convert(Decimal("1"), "M")[0] == Decimal("1")
    assert units.convert(Decimal("25"), "°C", temperature_kind="absolute")[0] == Decimal("298.15")
    with pytest.raises(ValueError): units.convert(Decimal("25"), "°C")
    with pytest.raises(ValueError): units.convert(Decimal("1"), "mM", dimension="mass_concentration")


def test_unknown_fields_references_and_cycles_rejected(tmp_path):
    (tmp_path / "bad.yaml").write_text("schema_version: registry-offline-v2.1\nentities: []\nunknown_field: true\n")
    with pytest.raises(RegistryError): Registry.from_paths(tmp_path)
    with pytest.raises(RegistryError): Registry([entity("one", "one", parent_id="missing")])
    with pytest.raises(RegistryError): Registry([entity("one", "one", redirect_to="two"), entity("two", "two", redirect_to="one")])
