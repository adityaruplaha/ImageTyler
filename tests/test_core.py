from __future__ import annotations

from pathlib import Path

from PIL import Image

from imagetyler.core import generate_tiled_pdf


def test_generate_tiled_pdf_creates_output(tmp_path: Path):
    image_path = tmp_path / "sample.png"
    output_pdf = tmp_path / "output.pdf"

    image = Image.new("RGB", (350, 450), color="white")
    image.save(image_path)

    result = generate_tiled_pdf(image_path=image_path, output_pdf=output_pdf)

    assert result == output_pdf
    assert output_pdf.exists()
    assert output_pdf.stat().st_size > 0
