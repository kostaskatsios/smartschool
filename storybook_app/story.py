from __future__ import annotations

from dataclasses import dataclass
from textwrap import fill
from typing import List

from .data import HeroOption, Idea
from .illustration import IllustrationStyle


@dataclass(frozen=True)
class Storybook:
    title: str
    style: IllustrationStyle
    pages: List[str]

    def as_text(self) -> str:
        header = [
            "=" * 60,
            f"Τίτλος: {self.title}",
            f"Στυλ εικονογράφησης: {self.style.name}",
            "=" * 60,
            "",
        ]
        body = []
        for idx, page in enumerate(self.pages, start=1):
            body.extend(
                [
                    f"Σελίδα {idx}",
                    "-" * 20,
                    fill(page, width=80),
                    "",
                ]
            )
        return "\n".join(header + body)


def _build_page_texts(idea: Idea, hero: HeroOption, style: IllustrationStyle) -> List[str]:
    base_tone = {
        "Ονειρικό Υδατογράφημα": "απαλό, ονειρικό φως",
        "Ζωηρές Κιμωλίες": "ζωηρές γραμμές και παιχνιδιάρικα χρώματα",
    }.get(style.name, "γεμάτες φαντασία εικόνες")

    pages = [
        (
            f"Η ιστορία ξεκινά όταν ο ήρωας {hero.title} κοιτά τον ουρανό και βλέπει "
            f"ένα σημάδι που μόνο εκείνος καταλαβαίνει. Το {base_tone} τον "
            f"προσκαλεί να ακολουθήσει το μυστήριο της ιστορίας ' {idea.title} '."
        ),
        (
            "Με θάρρος στην καρδιά, ο μικρός ήρωας συναντά φίλους που πιστεύουν "
            "στη δύναμη της καλοσύνης. Μαζί ανακαλύπτουν πως κάθε ψίθυρος "
            "κρύβει μια υπόσχεση." 
        ),
        (
            "Ένα απαλό τραγούδι οδηγεί την παρέα σε ένα μονοπάτι που "
            "λάμπει στο σκοτάδι. Κάθε βήμα γεμίζει τον αέρα με άρωμα "
            "από παιδικά όνειρα και αστέρια." 
        ),
        (
            "Κάποια στιγμή, ένα μικρό εμπόδιο κάνει τον ήρωα να διστάσει. "
            "Θυμάται όμως τα λόγια των φίλων του και βρίσκει μέσα του "
            "την πιο γλυκιά νότα θάρρους." 
        ),
        (
            "Με το νέο του κουράγιο, ο ήρωας χαρίζει το φως ή το τραγούδι του "
            "σε όποιον συναντά. Το μυστικό που έψαχνε ξεδιπλώνεται σαν "
            "σελίδα που φωτίζεται." 
        ),
        (
            "Στο τέλος, το χωριό γεμίζει με χαμόγελα και ιστορίες για να μοιράζεται. "
            "Ο ήρωας υπόσχεται να κρατήσει ζωντανό το θαύμα που έζησε, "
            "για να συνεχίσει να εμπνέει όλα τα παιδιά." 
        ),
    ]
    return pages


def create_storybook(idea: Idea, hero: HeroOption, style: IllustrationStyle) -> Storybook:
    pages = _build_page_texts(idea, hero, style)
    return Storybook(title=idea.title, style=style, pages=pages)
