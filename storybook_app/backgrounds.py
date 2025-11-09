from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw


@dataclass(frozen=True)
class BackgroundTheme:
    """Περιγραφή ενός φόντου εικονογράφησης."""

    name: str
    description: str
    palette: tuple[tuple[int, int, int], ...]
    overlay: str


def get_backgrounds() -> list[BackgroundTheme]:
    """Δίνει τις διαθέσιμες επιλογές φόντου."""

    return [
        BackgroundTheme(
            name="Παιχνιδιάρικο Ουράνιο Τόξο",
            description=(
                "Ζωντανές λωρίδες χρώματος και μικρά αστέρια που θυμίζουν"
                " πίνακα παιδικής χαράς. Δημιουργεί αίσθηση χαράς και"
                " περιπέτειας." 
            ),
            palette=((255, 205, 178), (255, 180, 210), (198, 234, 248), (255, 247, 153)),
            overlay="stars",
        ),
        BackgroundTheme(
            name="Κομψό Μινιμαλιστικό Στούντιο",
            description=(
                "Καθαρό, επαγγελματικό gradient με απαλές γωνίες και"
                " λεπτές λάμψεις. Ιδανικό για παρουσιάσεις και έντυπο υλικό." 
            ),
            palette=((240, 242, 245), (215, 222, 230), (190, 200, 210)),
            overlay="glow",
        ),
    ]


def _apply_palette(draw: ImageDraw.ImageDraw, size: tuple[int, int], palette: Iterable[tuple[int, int, int]]) -> None:
    """Ζωγραφίζει διαδοχικές οριζόντιες λωρίδες σύμφωνα με την παλέτα."""

    palette = list(palette)
    stripe_height = size[1] / max(len(palette), 1)
    for index, color in enumerate(palette):
        y0 = int(index * stripe_height)
        y1 = int((index + 1) * stripe_height)
        draw.rectangle([0, y0, size[0], y1], fill=color)


def _draw_starry_overlay(draw: ImageDraw.ImageDraw, size: tuple[int, int]) -> None:
    """Προσθέτει μικρά αστέρια για πιο παιδική αισθητική."""

    star_positions = [
        (size[0] * 0.2, size[1] * 0.25),
        (size[0] * 0.45, size[1] * 0.18),
        (size[0] * 0.65, size[1] * 0.3),
        (size[0] * 0.35, size[1] * 0.55),
        (size[0] * 0.75, size[1] * 0.6),
    ]
    for cx, cy in star_positions:
        draw.regular_polygon((cx, cy, 18), n_sides=5, fill=(255, 255, 255), rotation=18)


def _draw_glow_overlay(draw: ImageDraw.ImageDraw, size: tuple[int, int]) -> None:
    """Προσθέτει κυκλικές λάμψεις για πιο επαγγελματικό τόνο."""

    focus_points = [
        (size[0] * 0.3, size[1] * 0.35, 120),
        (size[0] * 0.7, size[1] * 0.55, 180),
    ]
    for cx, cy, radius in focus_points:
        for step, intensity in enumerate((240, 230, 220, 210), start=1):
            shrink = radius * (step / 4)
            bbox = [cx - shrink, cy - shrink, cx + shrink, cy + shrink]
            draw.ellipse(bbox, fill=(intensity, intensity, intensity))


def create_background_preview(output_dir: Path, theme: BackgroundTheme) -> Path:
    """Δημιουργεί προεπισκόπηση για το δοσμένο φόντο."""

    output_dir.mkdir(parents=True, exist_ok=True)
    size = (600, 400)
    image = Image.new("RGB", size, theme.palette[0])
    draw = ImageDraw.Draw(image)
    _apply_palette(draw, size, theme.palette)

    if theme.overlay == "stars":
        _draw_starry_overlay(draw, size)
    elif theme.overlay == "glow":
        _draw_glow_overlay(draw, size)

    filename = theme.name.lower().replace(" ", "_") + "_background.png"
    path = output_dir / filename
    image.save(path)
    return path
