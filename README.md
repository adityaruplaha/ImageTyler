# ImageTyler

[![BSD-3-Clause](https://img.shields.io/badge/license-BSD--3--Clause-blue.svg)](LICENSE)

ImageTyler tiles a source image across a PDF page for print-ready output. Entirely vibe-coded, but reviewed and tested by humans. It supports mixed-unit dimensions, padding, and cutting guides.

## Installation

Install as a standalone tool with `uv`:

```bash
uv tool install imagetyler
```

Add it as a dependency in your project:

```bash
uv add imagetyler
```

## CLI Usage

Basic usage:

```bash
imagetyler photo.jpg --size 35x45mm --paper A4
```

ImageTyler accepts mixed-unit dimensions and inherits missing units from either side of the `WxH` expression. These all work:

```bash
imagetyler photo.jpg --size 35x45mm --paper 210x297mm
imagetyler photo.jpg --size 35mmx45 --paper Letter
imagetyler photo.jpg --padding 2mm --landscape --border
```

Useful flags include `--padding` for spacing between tiles, `--landscape` for rotating the target page, and `--border` with `--border-width` for cutting guides.

Use `--list-units` to inspect supported measurement units and `--list-paper` to list recognized paper aliases.

## API Usage

```python
from pathlib import Path

from imagetyler import generate_tiled_pdf

output = generate_tiled_pdf(
    image_path=Path("photo.jpg"),
    output_pdf=Path("tiled_output.pdf"),
    paper="A4",
    image_size="35x45mm",
    padding="2mm",
)

print(output)
```

## License

ImageTyler is distributed under the BSD-3-Clause license.
