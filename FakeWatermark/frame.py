"""Render the bottom watermark bar onto an image using Pillow."""

from __future__ import annotations

from pathlib import Path
from typing import cast

from PIL import Image, ImageDraw, ImageFont

from manifest import Manifest

_PADDING = 14
_ZONE_GAP = 18
_LINE_SPACING = 6
_SEPARATOR_WIDTH = 2
_BAR_HEIGHT = 80
_BAR_COLOR = (255, 255, 255)
_TEXT_COLOR = (51, 51, 51)
_DIM_COLOR = (153, 153, 153)


def _load_font(size: int, font_path: Path | None = None) -> ImageFont.FreeTypeFont:
    """Load the configured font, then fall back to common system fonts and Pillow's default."""
    candidates = []
    if font_path is not None:
        candidates.append(str(font_path))
    candidates += ["arial.ttf", "segoeui.ttf", "DejaVuSans.ttf", "NotoSansCJK-Regular.ttc"]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return cast(ImageFont.FreeTypeFont, ImageFont.load_default(size))


def _load_logo(path: Path) -> tuple[Image.Image, int]:
    """Load and resize the logo, returning (image, width)."""
    logo = Image.open(path).convert("RGBA")
    target_height = _BAR_HEIGHT - 2 * _PADDING
    if target_height <= 0 or logo.height <= 0:
        return logo, 0
    width = max(1, round(logo.width * target_height / logo.height))
    return logo.resize((width, target_height)), width


def add_watermark(input_path: Path, output_path: Path, manifest: Manifest) -> None:
    """Append the watermark bar, then save the result to output_path.

    Layout (left to right):

        | device model |  logo |  | focal aperture exposure ISO |
        | capture time |       |  | GPS location (dim)          |
    """
    image = Image.open(input_path).convert("RGB")
    width, height = image.size
    frame = manifest.frame
    camera = manifest.camera
    bar_height = _BAR_HEIGHT

    canvas = Image.new("RGB", (width, height + bar_height), _BAR_COLOR)
    canvas.paste(image, (0, 0))
    draw = ImageDraw.Draw(canvas)

    big_font = _load_font(max(12, round(bar_height * 0.30)), frame.font_path)
    mid_font = _load_font(max(12, round(bar_height * 0.24)), frame.font_path)
    small_font = _load_font(max(12, round(bar_height * 0.18)), frame.font_path)

    brand_model = f"{camera.brand.upper()} {camera.model}"
    params = f"{camera.focal_length}  {camera.aperture}  {camera.exposure_time}  {camera.iso}"

    # --- Left zone: device model (big) and capture time (small, dim) ---
    left_width = round(max(
        draw.textlength(brand_model, font=big_font),
        draw.textlength(camera.capture_time, font=small_font),
    ))
    left_total = big_font.size + _LINE_SPACING + small_font.size
    left_y = height + (bar_height - left_total) // 2
    draw.text((_PADDING, left_y), brand_model, fill=_TEXT_COLOR, font=big_font)
    draw.text(
        (_PADDING, left_y + big_font.size + _LINE_SPACING),
        camera.capture_time,
        fill=_DIM_COLOR,
        font=small_font,
    )

    # --- Right zone: logo, separator, then params and GPS (right-aligned) ---
    logo, logo_width = _load_logo(frame.logo_path)
    text_width = round(max(
        draw.textlength(params, font=mid_font),
        draw.textlength(camera.location, font=small_font),
    ))
    text_x = width - _PADDING - text_width
    sep_x = text_x - _ZONE_GAP - _SEPARATOR_WIDTH
    logo_x = sep_x - _ZONE_GAP - logo_width

    canvas.paste(logo, (logo_x, height + _PADDING), logo)

    draw.line(
        [(sep_x, height + _PADDING), (sep_x, height + bar_height - _PADDING)],
        fill=_DIM_COLOR,
        width=_SEPARATOR_WIDTH,
    )

    right_total = mid_font.size + _LINE_SPACING + small_font.size
    text_y = height + (bar_height - right_total) // 2
    draw.text((text_x, text_y), params, fill=_TEXT_COLOR, font=mid_font)
    draw.text(
        (text_x, text_y + mid_font.size + _LINE_SPACING),
        camera.location,
        fill=_DIM_COLOR,
        font=small_font,
    )

    canvas.save(output_path)
