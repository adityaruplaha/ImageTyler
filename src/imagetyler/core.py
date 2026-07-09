from __future__ import annotations

import logging
from pathlib import Path

from .layout import calculate_grid_layout, validate_aspect_ratio
from .pdf import generate_pdf
from .parser import parse_dimensions, parse_length

logger = logging.getLogger(__name__)


def generate_tiled_pdf(
    image_path: Path | str,
    output_pdf: Path | str = Path("tiled_output.pdf"),
    paper: str = "A4",
    landscape: bool = False,
    image_size: str = "35x45mm",
    padding: str = "2mm",
    draw_border: bool = False,
    border_width: str = "2pt",
) -> Path:
    image_path = Path(image_path)
    output_pdf = Path(output_pdf)

    paper_width, paper_height = parse_dimensions(paper)
    if landscape:
        paper_width, paper_height = paper_height, paper_width

    img_width, img_height = parse_dimensions(image_size)
    padding_value = parse_length(padding)
    border_width_value = parse_length(border_width) if draw_border else 0.0

    validate_aspect_ratio(image_path, img_width, img_height, logger)

    grid = calculate_grid_layout(paper_width, paper_height, img_width, img_height, padding_value)
    generate_pdf(
        image_path=image_path,
        output_pdf=output_pdf,
        paper_size=(paper_width, paper_height),
        grid=grid,
        image_size=(img_width, img_height),
        padding=padding_value,
        draw_border=draw_border,
        border_width=border_width_value,
    )

    return output_pdf
