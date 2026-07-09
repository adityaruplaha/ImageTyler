from __future__ import annotations

import logging
from pathlib import Path

from PIL import Image

ASPECT_RATIO_TOLERANCE: float = 0.05


def calculate_grid_layout(
    paper_width: float,
    paper_height: float,
    img_width: float,
    img_height: float,
    padding: float,
) -> tuple[int, int, float, float]:
    cols = int((paper_width + padding) / (img_width + padding))
    rows = int((paper_height + padding) / (img_height + padding))

    if cols <= 0 or rows <= 0:
        raise ValueError("The specified image dimensions and padding exceed the paper size.")

    total_grid_width = (cols * img_width) + ((cols - 1) * padding)
    total_grid_height = (rows * img_height) + ((rows - 1) * padding)

    margin_x = (paper_width - total_grid_width) / 2.0
    margin_y = (paper_height - total_grid_height) / 2.0

    return cols, rows, margin_x, margin_y


def validate_aspect_ratio(
    image_path: Path,
    target_width: float,
    target_height: float,
    logger: logging.Logger,
    tolerance: float = ASPECT_RATIO_TOLERANCE,
) -> None:
    try:
        with Image.open(image_path) as img:
            native_width_px, native_height_px = img.size
            native_ratio = native_width_px / native_height_px
            target_ratio = target_width / target_height

            difference = abs((native_ratio / target_ratio) - 1.0)
            logger.debug(
                "Native aspect ratio: %.3f, Target aspect ratio: %.3f",
                native_ratio,
                target_ratio,
            )

            if difference > tolerance:
                logger.warning(
                    "ASPECT RATIO MISMATCH: The input image differs from the target dimensions by %.1f%%. "
                    "The image will be visibly stretched or squashed.",
                    difference * 100,
                )
    except Exception as exc:  # pragma: no cover - surface-level file/image failure
        raise ValueError(f"Failed to read image '{image_path}': {exc}") from exc
