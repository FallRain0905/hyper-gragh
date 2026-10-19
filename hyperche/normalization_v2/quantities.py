"""Explicit quantities with deterministic units and source-local occurrences."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, localcontext
from pathlib import Path
from typing import Any, Mapping
import unicodedata

import yaml

from .contracts import digest, stable_id


def number(value: Any) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ValueError("A scientific number must be an explicit finite decimal")
    try:
        parsed = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError("Invalid explicit decimal") from exc
    if not parsed.is_finite():
        raise ValueError("Non-finite scientific number")
    return parsed


def decimal_text(value: Decimal | None) -> str | None:
    if value is None:
        return None
    if value == 0:
        return "0"
    return format(value, "f").rstrip("0").rstrip(".") if "." in format(value, "f") else format(value, "f")


def unit_key(value: str) -> str:
    # Element/prefix case matters: mM, M, mV, and V cannot be case folded.
    return unicodedata.normalize("NFKC", value).replace("μ", "u").replace("µ", "u").replace("−", "-").strip()


@dataclass(frozen=True)
class Unit:
    symbol: str
    dimension: str
    base_unit: str
    scale: Decimal
    offset: Decimal = Decimal(0)
    temperature: bool = False


DEFAULT_UNITS = [
    {"symbol": "1", "aliases": ["fraction"], "dimension": "fraction", "base_unit": "1", "scale": "1"},
    {"symbol": "%", "aliases": ["percent"], "dimension": "fraction", "base_unit": "1", "scale": "0.01"},
    {"symbol": "g/L", "aliases": ["g L^-1"], "dimension": "mass_concentration", "base_unit": "g/L", "scale": "1"},
    {"symbol": "mg/L", "aliases": ["mg L^-1"], "dimension": "mass_concentration", "base_unit": "g/L", "scale": "0.001"},
    {"symbol": "ug/L", "aliases": ["μg/L", "µg/L", "ug L^-1"], "dimension": "mass_concentration", "base_unit": "g/L", "scale": "0.000001"},
    {"symbol": "mol/L", "aliases": ["M"], "dimension": "molar_concentration", "base_unit": "mol/L", "scale": "1"},
    {"symbol": "mmol/L", "aliases": ["mM"], "dimension": "molar_concentration", "base_unit": "mol/L", "scale": "0.001"},
    {"symbol": "s", "aliases": ["second", "seconds"], "dimension": "time", "base_unit": "s", "scale": "1"},
    {"symbol": "min", "aliases": ["minute", "minutes"], "dimension": "time", "base_unit": "s", "scale": "60"},
    {"symbol": "h", "aliases": ["hour", "hours"], "dimension": "time", "base_unit": "s", "scale": "3600"},
    {"symbol": "V", "aliases": [], "dimension": "voltage", "base_unit": "V", "scale": "1"},
    {"symbol": "mV", "aliases": [], "dimension": "voltage", "base_unit": "V", "scale": "0.001"},
    {"symbol": "A/cm2", "aliases": ["A/cm^2"], "dimension": "current_density", "base_unit": "A/cm2", "scale": "1"},
    {"symbol": "mA/cm2", "aliases": ["mA/cm^2", "mA cm^-2"], "dimension": "current_density", "base_unit": "A/cm2", "scale": "0.001"},
    {"symbol": "K", "aliases": [], "dimension": "temperature", "base_unit": "K", "scale": "1", "temperature": True},
    {"symbol": "C", "aliases": ["°C", "degC", "degc", "℃"], "dimension": "temperature", "base_unit": "K", "scale": "1", "offset": "273.15", "temperature": True},
    {"symbol": "Hz", "aliases": [], "dimension": "frequency", "base_unit": "Hz", "scale": "1"},
    {"symbol": "kHz", "aliases": [], "dimension": "frequency", "base_unit": "Hz", "scale": "1000"},
    {"symbol": "pH", "aliases": [], "dimension": "ph", "base_unit": "pH", "scale": "1"},
]


class UnitRegistry:
    def __init__(self, entries=None):
        self.entries = list(DEFAULT_UNITS if entries is None else entries)
        self.index: dict[str, Unit] = {}
        for row in self.entries:
            allowed = {"symbol", "aliases", "dimension", "base_unit", "scale", "offset", "temperature"}
            if set(row) - allowed or not all(row.get(k) for k in ("symbol", "dimension", "base_unit")):
                raise ValueError("Invalid unit registry declaration")
            scale = number(row.get("scale", "1"))
            offset = number(row.get("offset", "0"))
            if scale is None or offset is None or scale <= 0:
                raise ValueError("Unit scales must be finite and positive")
            unit = Unit(row["symbol"], row["dimension"], row["base_unit"], scale, offset, bool(row.get("temperature")))
            for alias in [row["symbol"], *row.get("aliases", [])]:
                key = unit_key(alias)
                if key in self.index and self.index[key] != unit:
                    raise ValueError("Conflicting unit alias")
                self.index[key] = unit
        self.snapshot_hash = digest(self.entries)

    @classmethod
    def from_yaml(cls, path: str | Path):
        payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or not isinstance(payload.get("units"), list):
            raise ValueError("Unit file must declare a units list")
        if any("factor" in row for row in payload["units"]):
            from .registry import Registry
            return cls.from_compiled(Registry.from_paths([path.parent / "base.yaml", path]))
        return cls(payload["units"])

    @classmethod
    def from_compiled(cls, registry):
        bases = {}
        for unit in registry.units.values():
            if number(unit.factor) == 1 and number(unit.offset) == 0:
                if unit.base_unit:
                    bases[unit.dimension] = unit.base_unit
                elif unit.dimension in bases:
                    raise ValueError("A unit dimension must have exactly one explicit base")
                else:
                    bases[unit.dimension] = unit.symbol
        rows = []
        for unit in registry.units.values():
            if unit.dimension not in bases:
                raise ValueError("Unit dimension is missing its explicit base")
            rows.append({"symbol": unit.symbol, "aliases": unit.aliases,
                         "dimension": unit.dimension, "base_unit": bases[unit.dimension],
                         "scale": unit.factor, "offset": unit.offset,
                         "temperature": unit.dimension in {"absolute_temperature", "temperature_difference"}})
        return cls(rows)

    def convert(self, value: Decimal, raw_unit: str, *, dimension: str | None = None,
                temperature_kind: str | None = None) -> tuple[Decimal, Unit]:
        unit = self.index.get(unit_key(raw_unit))
        if unit is None:
            raise ValueError("Unknown unit; preserve the original value")
        if dimension and unit.dimension != dimension:
            raise ValueError("Unit dimension conflicts with its metric")
        if unit.temperature and temperature_kind not in {"absolute", "difference"}:
            raise ValueError("Temperature conversion requires absolute/difference meaning")
        if unit.dimension == "temperature_difference" and temperature_kind != "difference":
            raise ValueError("A temperature difference is not an absolute temperature")
        offset = unit.offset if temperature_kind != "difference" else Decimal(0)
        with localcontext() as context:
            context.prec = 34
            return value * unit.scale + offset, unit


def observation(quantity: Mapping[str, Any], *, metric_id: str, roles: Mapping[str, list[str]],
                doc_id: str, revision_hash: str, chunk_id: str, local_id: str,
                context_id: str, units: UnitRegistry | None = None,
                dimension: str | None = None, bounds: tuple[str, str] | None = None) -> dict:
    """Normalize only explicit quantity fields; never scan description/formula digits.

    Unsupported scientific meanings remain original observations with a reason.
    Invalid numeric input is preserved for audit and cannot masquerade as a
    converted value. Two experiments with equal values retain different IDs.
    """
    if not all((metric_id, doc_id, revision_hash, chunk_id, local_id, context_id)):
        raise ValueError("An observation requires metric, provenance, local and experiment scope")
    raw = {k: quantity.get(k) for k in ("value", "value_min", "value_max", "unit")}
    result = {"metric_id": metric_id, "roles": {k: list(v) for k, v in roles.items()},
              "doc_id": doc_id, "revision_hash": revision_hash, "chunk_id": chunk_id,
              "local_id": local_id, "context_id": context_id, "raw": raw,
              "canonical": None, "status": "preserved_unresolved"}
    try:
        value, lower, upper = (number(raw[k]) for k in ("value", "value_min", "value_max"))
        if value is None and lower is None and upper is None:
            raise ValueError("No explicit local numeric field")
        if (lower is None) != (upper is None) or (value is not None and lower is not None):
            raise ValueError("A quantity requires either one scalar or one complete range")
        if lower is not None and lower > upper:
            raise ValueError("Range bounds are reversed")
        raw_unit = str(raw["unit"] or "")
        if not raw_unit:
            raise ValueError("A unit is required; dimensionless quantities must explicitly use 1")
        registry = units or UnitRegistry()
        values = [value] if value is not None else [lower, upper]
        converted = [registry.convert(v, raw_unit, dimension=dimension,
                                      temperature_kind=quantity.get("temperature_kind")) for v in values]
        unit = converted[0][1]
        numeric = [pair[0] for pair in converted]
        if bounds and any(v < Decimal(bounds[0]) or v > Decimal(bounds[1]) for v in numeric):
            raise ValueError("Quantity outside explicitly declared metric bounds")
        if unit.dimension == "ph" and any(v < 0 or v > 14 for v in numeric):
            raise ValueError("pH outside the configured aqueous benchmark bounds")
        result["canonical"] = {"value": decimal_text(numeric[0]) if value is not None else None,
                               "value_min": decimal_text(numeric[0]) if lower is not None else None,
                               "value_max": decimal_text(numeric[1]) if upper is not None else None,
                               "unit": unit.base_unit, "dimension": unit.dimension,
                               "unit_policy_hash": digest(unit.__dict__),
                               "temperature_kind": quantity.get("temperature_kind")}
        result["status"] = "normalized_explicit"
    except (ValueError, TypeError, InvalidOperation) as exc:
        result["reason"] = str(exc)
    # Hash raw identity even when a scientific value is invalid/non-finite;
    # rejected values are represented as text rather than illegal JSON NaN.
    identity = {**result, "raw": {k: str(v) if isinstance(v, (float, Decimal)) else v for k, v in raw.items()}}
    result["raw"] = identity["raw"]
    result["observation_id"] = stable_id("observation", identity)
    return result
