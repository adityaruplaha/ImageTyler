from __future__ import annotations

import math

from reportlab.lib import pagesizes, units

from imagetyler.parser import parse_dimensions, parse_length


def test_parse_dimensions_inherits_units_from_right():
    width, height = parse_dimensions("35x45mm")
    assert math.isclose(width, 35 * units.mm)
    assert math.isclose(height, 45 * units.mm)


def test_parse_dimensions_inherits_units_from_left():
    width, height = parse_dimensions("35mmx45")
    assert math.isclose(width, 35 * units.mm)
    assert math.isclose(height, 45 * units.mm)


def test_parse_dimensions_accepts_pagesize_alias():
    width, height = parse_dimensions("A4")
    assert (width, height) == pagesizes.A4


def test_parse_length_defaults_to_millimeters():
    assert math.isclose(parse_length("2"), 2 * units.mm)
