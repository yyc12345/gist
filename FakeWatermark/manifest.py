"""Load and validate the fake-watermark TOML manifest."""

from __future__ import annotations

import tomllib
from pathlib import Path

from pydantic import BaseModel, Field


class Camera(BaseModel):
    """Camera-related fields read from the [camera] section."""

    capture_time: str = Field(description="Capture time, e.g. '2025-07-18 14:32:05'")
    brand: str = Field(description="Camera brand, e.g. 'Xiaomi'")
    model: str = Field(description="Camera model, e.g. 'Xiaomi 17'")
    focal_length: str = Field(description="Focal length, e.g. '6.6mm'")
    aperture: str = Field(description="Aperture, e.g. 'F1.7'")
    exposure_time: str = Field(description="Exposure time, e.g. '1/30s'")
    iso: str = Field(description="ISO value, e.g. 'ISO32'")
    location: str = Field(
        description="Geographic location in DMS, e.g. '40°3'13\"N 116°19'25\"E'"
    )


class Frame(BaseModel):
    """Frame-related fields read from the [frame] section."""

    logo_path: Path = Field(description="Path to the logo image shown in the bottom bar")
    font_path: Path = Field(description="Path to the TrueType font used for the bar text")


class Manifest(BaseModel):
    """Validated content of a watermark manifest file."""

    camera: Camera
    frame: Frame


def load(path: Path) -> Manifest:
    """Read a TOML manifest file and validate it against the Manifest schema."""
    with path.open("rb") as fh:
        data = tomllib.load(fh)
    manifest = Manifest.model_validate(data)
    for attr in ("logo_path", "font_path"):
        value = getattr(manifest.frame, attr)
        if not value.is_absolute():
            setattr(manifest.frame, attr, path.parent / value)
    return manifest
