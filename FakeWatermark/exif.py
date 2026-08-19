"""Clear and rewrite image EXIF data using the exiftool command line tool."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

from manifest import Manifest

_NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")
_SLASH_RE = re.compile(r"(\d+)\s*/\s*(\d+)")
_LOCATION_RE = re.compile(
    r"(?P<lat>\d{1,3})\s*°(?:(?P<lat_m>\d{1,2})\s*')?(?:(?P<lat_s>\d{1,2}(?:\.\d+)?)\s*\")?"
    r"\s*(?P<lat_ref>[NS])"
    r"[,\s]+"
    r"(?P<lon>\d{1,3})\s*°(?:(?P<lon_m>\d{1,2})\s*')?(?:(?P<lon_s>\d{1,2}(?:\.\d+)?)\s*\")?"
    r"\s*(?P<lon_ref>[EW])",
    re.IGNORECASE,
)

_ENV_EXIFTOOL = "FAKE_WATERMARK_EXIFTOOL_BIN"


def exiftool_bin() -> str:
    """Return the exiftool binary path, overridable via the environment."""
    return os.environ.get(_ENV_EXIFTOOL, "exiftool")


def _run_exiftool(args: list[str]) -> None:
    """Run exiftool with the given arguments, raising on a non-zero exit."""
    proc = subprocess.Popen(
        [exiftool_bin(), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(
            f"exiftool failed with exit code {proc.returncode}\n"
            f"stdout: {stdout}\n"
            f"stderr: {stderr}"
        )


def _as_number(value: str) -> str:
    """Extract a plain number from a value such as 'F1.7' or 'ISO32'."""
    match = _NUMBER_RE.search(value)
    if not match:
        raise ValueError(f"Could not parse a numeric value from {value!r}")
    return match.group(0)


def _as_exposure(value: str) -> str:
    """Normalize a value such as '1/30s' to a fraction such as '1/30'."""
    match = _SLASH_RE.search(value)
    if match:
        return f"{match.group(1)}/{match.group(2)}"
    return _as_number(value)


def _as_focal_length(value: str) -> str:
    """Normalize a value such as '6.6mm' to '6.6 mm'."""
    return f"{_as_number(value)} mm"


def _as_datetime(value: str) -> str:
    """Convert 'YYYY-MM-DD HH:MM:SS' into the 'YYYY:MM:DD HH:MM:SS' EXIF format."""
    return value.replace("-", ":")


def _as_location(value: str) -> tuple[tuple[str, str], tuple[str, str]] | None:
    """Parse a DMS location and return ((lat DMS, lat ref), (lon DMS, lon ref))."""

    def part(match: re.Match[str], prefix: str) -> tuple[str, str]:
        degrees = match.group(prefix)
        minutes = match.group(f"{prefix}_m") or "0"
        seconds = match.group(f"{prefix}_s") or "0"
        return f"{degrees} {minutes} {seconds}", match.group(f"{prefix}_ref").upper()

    match = _LOCATION_RE.search(value)
    if not match:
        return None
    return part(match, "lat"), part(match, "lon")


def clear_exif(path: Path) -> None:
    """Strip every metadata tag from the given image in place."""
    _run_exiftool(["-overwrite_original", "-all=", str(path)])


def write_watermark(path: Path, manifest: Manifest) -> None:
    """Write the camera watermark data into the image EXIF in place."""
    camera = manifest.camera
    args = [
        "-overwrite_original",
        f"-AllDates={_as_datetime(camera.capture_time)}",
        f"-Make={camera.brand}",
        f"-Model={camera.model}",
        f"-FocalLength={_as_focal_length(camera.focal_length)}",
        f"-FNumber={_as_number(camera.aperture)}",
        f"-ExposureTime={_as_exposure(camera.exposure_time)}",
        f"-ISO={_as_number(camera.iso)}",
    ]
    location = _as_location(camera.location)
    if location is None:
        raise ValueError(f"Could not parse geographic location from {camera.location!r}")
    (lat_dms, lat_ref), (lon_dms, lon_ref) = location
    args += [
        f"-GPSLatitude={lat_dms}",
        f"-GPSLatitudeRef={lat_ref}",
        f"-GPSLongitude={lon_dms}",
        f"-GPSLongitudeRef={lon_ref}",
    ]
    args.append(str(path))
    _run_exiftool(args)
