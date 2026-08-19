"""Command line interface for fake-watermark."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Cli:
    """Frozen container for parsed command line arguments."""

    manifest: Path
    input: Path
    output: Path


def parse() -> Cli:
    """Build the argument parser, parse the command line and return a Cli."""
    parser = argparse.ArgumentParser(
        prog="fake-watermark",
        description="Stamp a fake camera watermark onto a photo and write matching EXIF data.",
    )
    parser.add_argument(
        "-m",
        "--manifest",
        dest="manifest",
        action="store",
        type=Path,
        required=True,
        help="Path to the TOML manifest that defines the watermark content",
        metavar="MANIFEST.TOML",
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="input",
        action="store",
        type=Path,
        required=True,
        help="Path to the source image file",
        metavar="INPUT.IMAGE",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        action="store",
        type=Path,
        required=True,
        help="Path where the watermarked image will be written",
        metavar="OUTPUT.IMAGE",
    )
    args = parser.parse_args()
    return Cli(manifest=args.manifest, input=args.input, output=args.output)
