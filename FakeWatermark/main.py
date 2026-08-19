"""Entry point that ties together the cli, manifest, frame and exif modules."""

from __future__ import annotations

from cli import parse
from exif import clear_exif, write_watermark
from frame import add_watermark
from manifest import load


def main() -> None:
    """Run the whole fake-watermark pipeline."""
    cli = parse()
    manifest = load(cli.manifest)
    add_watermark(cli.input, cli.output, manifest)
    clear_exif(cli.output)
    write_watermark(cli.output, manifest)


if __name__ == "__main__":
    main()
