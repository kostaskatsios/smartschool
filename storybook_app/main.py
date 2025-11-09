from __future__ import annotations

from pathlib import Path

from .data import IDEAS, HeroOption, Idea
from .illustration import IllustrationStyle, create_preview, get_styles
from .story import create_storybook


def _prompt_choice(prompt: str, options: list[str]) -> int:
    print(prompt)
    for idx, option in enumerate(options, start=1):
        print(f"  {idx}. {option}")

    while True:
        choice = input("Επιλογή (γράψε τον αριθμό): ").strip()
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(options):
                return index
        print("Παρακαλώ διάλεξε έναν από τους διαθέσιμους αριθμούς.")


def choose_idea() -> Idea:
    options = [f"{idea.title} — {idea.summary}" for idea in IDEAS]
    idx = _prompt_choice("Διάλεξε μια ιδέα παραμυθιού:", options)
    return IDEAS[idx]


def choose_hero(idea: Idea) -> HeroOption:
    options = [
        f"{hero.title}: {hero.description}" for hero in idea.hero_options
    ]
    idx = _prompt_choice(
        "Επίλεξε τον ήρωα και την πλοκή (κάθε πρόταση έχει 2-3 προτάσεις):",
        options,
    )
    return idea.hero_options[idx]


def choose_style(idea: Idea, hero: HeroOption) -> IllustrationStyle:
    styles = get_styles()
    output_dir = Path("previews")
    print("\nΔιαθέσιμα στυλ εικονογράφησης με δείγματα:")
    for idx, style in enumerate(styles, start=1):
        path = create_preview(output_dir, style, idea.title, hero.title)
        print(f"  {idx}. {style.name}")
        print(f"     Περιγραφή: {style.description}")
        print(f"     Προεπισκόπηση: {path}")

    idx = _prompt_choice("Ποιο στυλ σου ταιριάζει;", [s.name for s in styles])
    return styles[idx]


def main() -> None:
    print("Καλωσήρθες στον δημιουργό παραμυθιών!")
    idea = choose_idea()
    print(f"\nΔιάλεξες: {idea.title}\n")
    hero = choose_hero(idea)
    print(f"\nΥπέροχα! Ο ήρωας σου είναι: {hero.title}\n")
    style = choose_style(idea, hero)

    storybook = create_storybook(idea, hero, style)
    print("\nΤο παραμύθι σου είναι έτοιμο:\n")
    print(storybook.as_text())


if __name__ == "__main__":
    main()
