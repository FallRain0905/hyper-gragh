"""Type-aware text policies for registry lookup keys.

A lookup key is *not* an identity decision.  It only narrows the registry
index; scope, guards and the declared identity policy still decide whether a
mention may bind.  Two normalizers are deliberately different:

``common_name``
    Unicode NFC, case-folding, dash/whitespace canonicalisation.  It never
    strips or folds superscripts/subscripts.

``chemical_formula``
    Preserves element case and the difference between stoichiometric
    subscripts and charge superscripts.  Subscript digits become ordinary
    digits (``H₂SO₄`` == ``H2SO4``) while superscripts stay in explicit
    ``^{...}`` markers.  Thus ``VO²⁺`` (charge 2+) and ``VO₂⁺`` (two oxygens,
    charge 1+) remain distinct, and ``Co`` (cobalt) remains distinct from
    ``CO`` (carbon monoxide).

``exact`` compares the NFC text after whitespace trimming and is intended for
identifiers that must not be case-folded at all.
"""

from __future__ import annotations

import re
import unicodedata

POLICIES = ("common_name", "chemical_formula", "exact")

_CHEMICAL_KINDS = frozenset(
    {
        "chemical",
        "compound",
        "catalyst",
        "complex",
        "electrode_material",
        "ion",
        "material",
        "membrane_material",
        "mixture",
        "molecule",
        "polymer",
        "radical",
        "species",
    }
)

_SUPERSCRIPT_MAP = {
    "⁰": "0",
    "¹": "1",
    "²": "2",
    "³": "3",
    "⁴": "4",
    "⁵": "5",
    "⁶": "6",
    "⁷": "7",
    "⁸": "8",
    "⁹": "9",
    "⁺": "+",
    "⁻": "-",
}
_SUBSCRIPT_MAP = {
    "₀": "0",
    "₁": "1",
    "₂": "2",
    "₃": "3",
    "₄": "4",
    "₅": "5",
    "₆": "6",
    "₇": "7",
    "₈": "8",
    "₉": "9",
    "₊": "+",
    "₋": "-",
}

_DASHES = "\u2010\u2011\u2012\u2013\u2014\u2015\u2212"
_DASH_TRANSLATION = str.maketrans({character: "-" for character in _DASHES})

# Element symbols used only to recognise a compact token as a chemical
# formula.  The list is not used to infer chemistry; it prevents case-folding
# from collapsing tokens such as "Co" (cobalt) and "CO" (carbon monoxide).
_ELEMENTS = frozenset(
    """
    H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni
    Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe
    Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au
    Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf
    Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og
    """.split()
)
_SUBSCRIPTS = frozenset(_SUBSCRIPT_MAP)
_SUPERSCRIPTS = frozenset(_SUPERSCRIPT_MAP)


def _parse_formula_token(value: str) -> list[str] | None:
    """Return element symbols when ``value`` is one compact formula token."""

    if not value or any(character.isspace() for character in value):
        return None
    symbols: list[str] = []
    index = 0
    length = len(value)
    while index < length:
        character = value[index]
        if character.isdigit() or character in _SUBSCRIPTS or character in _SUPERSCRIPTS:
            index += 1
            continue
        if character in "+-^":
            index += 1
            continue
        if not character.isupper():
            return None
        symbol = character
        index += 1
        if index < length and value[index].islower():
            symbol += value[index]
            index += 1
        if symbol not in _ELEMENTS:
            return None
        symbols.append(symbol)
        while index < length and (value[index].isdigit() or value[index] in _SUBSCRIPTS):
            index += 1
    return symbols or None


def _preserve_chemical_case(value: str) -> bool:
    """Keep case for tokens where folding would erase a chemical distinction.

    A bare all-capital abbreviation ("HER", "PFBS") still case-folds so prose
    matching keeps working.  A token that contains a two-letter element symbol
    ("Co", "Cr", "In") or explicit stoichiometry/charge ("H2O", "VO²⁺") keeps
    its case; this is what separates ``Co`` from ``CO``.
    """

    symbols = _parse_formula_token(value)
    if symbols is None:
        return False
    has_two_letter_symbol = any(len(symbol) == 2 for symbol in symbols)
    has_stoichiometry_or_charge = any(
        character.isdigit()
        or character in _SUBSCRIPTS
        or character in _SUPERSCRIPTS
        or character in "+-^"
        for character in value
    )
    return has_two_letter_symbol or has_stoichiometry_or_charge


def _require_policy(policy: str) -> str:
    if policy not in POLICIES:
        raise ValueError(
            f"Unknown text policy {policy!r}; expected one of {', '.join(POLICIES)}"
        )
    return policy


def default_normalizer_for_kind(kind: str) -> str:
    """Return the default alias normalizer for an object kind."""

    return "chemical_formula" if str(kind).strip().lower() in _CHEMICAL_KINDS else "common_name"


def _normalize_common_name(text: str) -> str:
    value = unicodedata.normalize("NFC", str(text))
    value = value.replace("\u00a0", " ").replace("\u202f", " ")
    value = value.translate(_DASH_TRANSLATION)
    value = value.replace("•", "·").replace("∙", "·")
    # A hyphen between two word characters is a formatting choice
    # ("iron-chromium").  A leading/trailing hyphen is a charge sign
    # ("PFBS-") and must not become a separator.
    value = re.sub(r"(?<=[A-Za-z0-9])\s*-\s*(?=[A-Za-z0-9])", " ", value)
    value = re.sub(r"\s*/\s*", "/", value)
    value = re.sub(r"\s+", " ", value).strip()
    if _preserve_chemical_case(value):
        return value
    return value.casefold()


def _normalize_formula_script(value: str) -> str:
    """Convert Unicode scripts into explicit, meaning-preserving markers."""

    output: list[str] = []
    index = 0
    length = len(value)
    while index < length:
        character = value[index]
        if character in _SUPERSCRIPT_MAP:
            end = index
            mapped: list[str] = []
            while end < length and value[end] in _SUPERSCRIPT_MAP:
                mapped.append(_SUPERSCRIPT_MAP[value[end]])
                end += 1
            output.append("^{" + "".join(mapped) + "}")
            index = end
            continue
        if character in _SUBSCRIPT_MAP:
            end = index
            mapped = []
            while end < length and value[end] in _SUBSCRIPT_MAP:
                mapped.append(_SUBSCRIPT_MAP[value[end]])
                end += 1
            script = "".join(mapped)
            # Subscript digits express stoichiometry and are equivalent to the
            # ordinary digits used by plain-text formulas.  Subscript signs or
            # letters are not ordinary stoichiometry and stay marked.
            if script.isdigit():
                output.append(script)
            else:
                output.append("_{" + script + "}")
            index = end
            continue
        output.append(character)
        index += 1
    return "".join(output)


def _normalize_chemical_formula(text: str) -> str:
    value = unicodedata.normalize("NFC", str(text))
    value = value.translate(_DASH_TRANSLATION)
    value = value.replace("＋", "+")
    value = value.replace("•", "·").replace("∙", "·")
    # A leading period is a common ASCII radical notation (".OH"); keep decimal
    # points and file-like dots untouched.
    value = re.sub(r"(?<![0-9A-Za-z])\.(?=[A-Z])", "·", value)
    value = _normalize_formula_script(value)
    value = re.sub(r"\s+", "", value)
    # Canonicalise caret notation ("VO^2+") into the same marker used for
    # Unicode superscripts ("VO²⁺").
    value = re.sub(
        r"\^(?!\{)\s*([0-9]*[+\-]?)",
        lambda match: "^{" + match.group(1) + "}" if match.group(1) else "^",
        value,
    )
    # Join adjacent script runs: "^{2}^{+}" -> "^{2+}".
    previous = None
    while previous != value:
        previous = value
        value = re.sub(r"\^\{([^{}]*)\}\^\{([^{}]*)\}", r"^{\1\2}", value)
        value = re.sub(r"_\{([^{}]*)\}_\{([^{}]*)\}", r"_{\1\2}", value)
    return value


def normalize(text: str, policy: str = "common_name") -> str:
    """Return the declared lookup key for ``text`` under ``policy``."""

    _require_policy(policy)
    if text is None:
        raise ValueError("text must not be None")
    if policy == "common_name":
        return _normalize_common_name(text)
    if policy == "chemical_formula":
        return _normalize_chemical_formula(text)
    return unicodedata.normalize("NFC", str(text)).strip()


def fuzzy_key(text: str, policy: str = "common_name") -> str:
    """Return a candidate-retrieval key that can never prove identity.

    The ``fuzzy:`` prefix keeps this key out of the exact identity index, so a
    caller cannot accidentally treat a punctuation-insensitive match as a
    declaration of sameness.  Fuzzy keys are only useful for building review
    candidates.
    """

    _require_policy(policy)
    base = normalize(text, policy)
    collapsed = re.sub(r"[\W_]+", "", base, flags=re.UNICODE)
    return "fuzzy:" + collapsed
