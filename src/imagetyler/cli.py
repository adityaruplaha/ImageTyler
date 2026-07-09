from __future__ import annotations

import logging
from pathlib import Path
from typing import Annotated, Optional

import typer

from .core import generate_tiled_pdf
from .parser import AVAILABLE_PAGESIZES, AVAILABLE_UNITS

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

app = typer.Typer(
    help="Automagically tile images onto a PDF page using regex dimension parsing.",
    add_completion=True,
)


def setup_logger(verbose: bool) -> logging.Logger:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format=LOG_FORMAT, datefmt=DATE_FORMAT)
    return logging.getLogger(__name__)


def list_units_callback(value: bool) -> None:
    if value:
        typer.echo("Supported measurement units (case-insensitive):")
        typer.echo(f"  {', '.join(sorted(AVAILABLE_UNITS.keys()))}")
        raise typer.Exit()


def list_paper_callback(value: bool) -> None:
    if value:
        typer.echo("Supported paper size aliases (case-insensitive):")
        typer.echo(f"  {', '.join(sorted(AVAILABLE_PAGESIZES.keys()))}")
        raise typer.Exit()


@app.command()
def tile_image(
    image_path: Annotated[
        Optional[Path],
        typer.Argument(
            help="Path to the input image file (JPEG, PNG, etc).",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
    ] = None,
    output_pdf: Annotated[
        Path,
        typer.Option("--output", "-o", help="Path to save the generated PDF file.", writable=True),
    ] = Path("tiled_output.pdf"),
    paper: Annotated[
        str,
        typer.Option(
            "--paper",
            "-p",
            help="Paper size alias (e.g., A4) or explicit dimensions (e.g., 210x297mm).",
        ),
    ] = "A4",
    landscape: Annotated[
        bool,
        typer.Option(
            "--landscape",
            "-l",
            help="Rotate the target paper orientation to landscape.",
        ),
    ] = False,
    image_size: Annotated[
        str,
        typer.Option(
            "--size",
            "-s",
            help="Target image size formatted as WxH with optional mixed units.",
        ),
    ] = "35x45mm",
    padding_str: Annotated[
        str, typer.Option("--padding", help="Minimum padding between images.")
    ] = "2mm",
    draw_border: Annotated[
        bool,
        typer.Option(
            "--border",
            "-b",
            help="Draw a solid black border around each image for ease of cutting.",
        ),
    ] = False,
    border_width_str: Annotated[
        str,
        typer.Option(
            "--border-width",
            help="Width of the border if enabled, supporting standard units.",
        ),
    ] = "2pt",
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Enable verbose debug logging.")
    ] = False,
    list_units: Annotated[
        bool,
        typer.Option(
            "--list-units",
            help="List all supported measurement units (case-insensitive) and exit.",
            callback=list_units_callback,
            is_eager=True,
        ),
    ] = False,
    list_paper: Annotated[
        bool,
        typer.Option(
            "--list-paper",
            help="List all supported paper size aliases (case-insensitive) and exit.",
            callback=list_paper_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    if not image_path:
        typer.echo(
            "Error: Missing argument 'IMAGE_PATH'. Use --help for usage details.",
            err=True,
        )
        raise typer.Exit(code=1)

    setup_logger(verbose)

    try:
        generate_tiled_pdf(
            image_path=image_path,
            output_pdf=output_pdf,
            paper=paper,
            landscape=landscape,
            image_size=image_size,
            padding=padding_str,
            draw_border=draw_border,
            border_width=border_width_str,
        )
    except (ValueError, RuntimeError) as exc:
        logging.getLogger(__name__).error(str(exc))
        raise typer.Exit(code=1) from exc

    logging.getLogger(__name__).info("Successfully generated PDF: '%s'", output_pdf)


if __name__ == "__main__":
    app()
