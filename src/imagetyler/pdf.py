from __future__ import annotations

import logging
from pathlib import Path

from reportlab.pdfgen import canvas


def generate_pdf(
    image_path: Path,
    output_pdf: Path,
    paper_size: tuple[float, float],
    grid: tuple[int, int, float, float],
    image_size: tuple[float, float],
    padding: float,
    draw_border: bool,
    border_width: float,
) -> None:
    cols, rows, margin_x, margin_y = grid
    img_width, img_height = image_size

    try:
        pdf_canvas = canvas.Canvas(str(output_pdf), pagesize=paper_size)

        for row in range(rows):
            for col in range(cols):
                x_pos = margin_x + (col * (img_width + padding))
                y_pos = margin_y + (row * (img_height + padding))

                pdf_canvas.drawImage(
                    str(image_path), x_pos, y_pos, width=img_width, height=img_height
                )

                if draw_border:
                    pdf_canvas.setLineWidth(border_width)
                    pdf_canvas.setStrokeColorRGB(0, 0, 0)
                    pdf_canvas.rect(x_pos, y_pos, img_width, img_height, stroke=1, fill=0)

        pdf_canvas.showPage()
        pdf_canvas.save()
    except Exception as exc:
        raise RuntimeError(f"An error occurred while generating the PDF: {exc}") from exc
