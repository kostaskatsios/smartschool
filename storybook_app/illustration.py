from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class IllustrationStyle:
    name: str
    description: str
    background: tuple[int, int, int]
    accent: tuple[int, int, int]
    text_color: tuple[int, int, int]


def get_styles() -> list[IllustrationStyle]:
    """Δίνει δύο βασικά στυλ εικονογράφησης."""

    return [
        IllustrationStyle(
            name="Ονειρικό Υδατογράφημα",
            description=(
                "Απαλές πινελιές και διάφανα χρώματα σαν να αιωρούνται σε σύννεφο. "
                "Ιδανικό για τρυφερές, μελωδικές σκηνές."
            ),
            background=(188, 212, 241),
            accent=(230, 240, 255),
            text_color=(25, 50, 90),
        ),
        IllustrationStyle(
            name="Ζωηρές Κιμωλίες",
            description=(
                "Παιχνιδιάρικες γραμμές και ζεστές αντιθέσεις σαν πίνακας "
                "σε σχολικό πίνακα. Δίνει ενέργεια και ρυθμό."
            ),
            background=(255, 235, 205),
            accent=(255, 180, 120),
            text_color=(80, 30, 20),
        ),
    ]


def create_preview(
    output_dir: Path,
    style: IllustrationStyle,
    idea_title: str,
    hero_title: str,
) -> Path:
    """Δημιουργεί μια απλή προεπισκόπηση εικόνας για το στυλ."""

    output_dir.mkdir(parents=True, exist_ok=True)
    size = (600, 400)
    image = Image.new("RGB", size, style.background)
    draw = ImageDraw.Draw(image)

    # Δευτερεύον σύννεφο/σχήμα για αίσθηση βάθους
    accent_box = [
        size[0] * 0.1,
        size[1] * 0.15,
        size[0] * 0.9,
        size[1] * 0.85,
    ]
    draw.rounded_rectangle(accent_box, radius=40, fill=style.accent)

    # Φωτεινές πινελιές
    for offset in range(3):
        draw.ellipse(
            [
                size[0] * 0.15 + offset * 80,
                size[1] * 0.2 + offset * 20,
                size[0] * 0.3 + offset * 80,
                size[1] * 0.35 + offset * 20,
            ],
            fill=(255, 255, 255, 180),
        )

    font = ImageFont.load_default()
    text = f"{idea_title}\n{hero_title}\n{style.name}"
    draw.multiline_text(
        (size[0] * 0.5, size[1] * 0.5),
        text,
        font=font,
        fill=style.text_color,
        anchor="mm",
        align="center",
        spacing=8,
    )

    filename = f"{style.name.lower().replace(' ', '_')}.png"
    path = output_dir / filename
    image.save(path)
    return path


def summarize_styles(
    styles: Iterable[IllustrationStyle],
) -> list[str]:
    """Επιστρέφει κείμενα παρουσίασης των στυλ."""

    summaries = []
    for style in styles:
        summaries.append(
            f"- {style.name}: {style.description}"
        )
    return summaries
