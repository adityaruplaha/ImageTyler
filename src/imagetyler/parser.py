from __future__ import annotations

import inspect
import re

from reportlab.lib import pagesizes, units

AVAILABLE_UNITS: dict[str, float] = {
    name.lower(): value
    for name, value in inspect.getmembers(units)
    if not name.startswith("_") and isinstance(value, (int, float))
}
AVAILABLE_UNITS["pt"] = 1.0

AVAILABLE_PAGESIZES: dict[str, tuple[float, float]] = {
    name.lower(): value
    for name, value in inspect.getmembers(pagesizes)
    if not name.startswith("_") and isinstance(value, tuple) and len(value) == 2
}

DEFAULT_PAPER_STR: str = "A4"
DEFAULT_IMAGE_SIZE_STR: str = "35x45mm"
DEFAULT_PADDING_STR: str = "2mm"
DEFAULT_UNIT_STR: str = "mm"
DEFAULT_BORDER_WIDTH_STR: str = "2pt"


def parse_dimensions(val: str) -> tuple[float, float]:
    """Parse a `WxH` string or paper alias into points."""

    clean_val = re.sub(r"\s+", "", val.lower())

    if clean_val in AVAILABLE_PAGESIZES:
        return AVAILABLE_PAGESIZES[clean_val]

    match = re.match(r"^([\d.]+)([a-z]*)x([\d.]+)([a-z]*)$", clean_val)
    if not match:
        raise ValueError(
            f"Invalid dimension format: '{val}'. Expected 'WxH' or a standard paper alias."
        )

    w_num_str, w_unit_str, h_num_str, h_unit_str = match.groups()

    if not w_unit_str and not h_unit_str:
        resolved_w_unit = DEFAULT_UNIT_STR
        resolved_h_unit = DEFAULT_UNIT_STR
    elif not w_unit_str:
        resolved_w_unit = h_unit_str
        resolved_h_unit = h_unit_str
    elif not h_unit_str:
        resolved_w_unit = w_unit_str
        resolved_h_unit = w_unit_str
    else:
        resolved_w_unit = w_unit_str
        resolved_h_unit = h_unit_str

    if resolved_w_unit not in AVAILABLE_UNITS:
        raise ValueError(f"Unknown unit for width: '{resolved_w_unit}'")
    if resolved_h_unit not in AVAILABLE_UNITS:
        raise ValueError(f"Unknown unit for height: '{resolved_h_unit}'")

    return float(w_num_str) * AVAILABLE_UNITS[resolved_w_unit], float(h_num_str) * AVAILABLE_UNITS[
        resolved_h_unit
    ]


def parse_length(val: str) -> float:
    """Parse a single length string into points."""

    clean_val = re.sub(r"\s+", "", val.lower())
    match = re.match(r"^([\d.]+)([a-z]*)$", clean_val)
    if not match:
        raise ValueError(f"Cannot parse length value: '{val}'")

    num_str, unit_str = match.groups()
    resolved_unit = unit_str if unit_str else DEFAULT_UNIT_STR

    if resolved_unit not in AVAILABLE_UNITS:
        raise ValueError(f"Unknown unit: '{resolved_unit}'")

    return float(num_str) * AVAILABLE_UNITS[resolved_unit]
