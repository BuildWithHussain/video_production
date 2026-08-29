"""Generate one question-card composition per Q&A beat in a training edit.

`compositions/q-doppio.html` is the reference card: lower third, brand-accent
`Q`, damped-spring entrance, hold, ease-in exit. Everything except the question
text and the hold length is identical between cards, so the cards are stamped
from that file rather than hand-copied.

The hold length is NOT free: a card's `data-duration` has to equal the OUTPUT
window it covers, which is shorter than the source span wherever the auto-cut
trimmed silence inside it. So the durations come from `final_cut.json`, after
`apply_edits.py` has mapped each card onto the finished timeline.

    python make_q_cards.py ../projects/agentic-ai-development/day-4/edit/final_cut.json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
OUT_DIR = ROOT / "compositions"

# A card's `kind` picks the template. `q` is the question card; `ref` is the
# same geometry and motion with a REPO tag and a mono URL, for the places where
# a project is named wrong on the recording or only mentioned in passing.
TEMPLATES = {
    "q": ROOT / "compositions" / "q-doppio.html",
    "ref": ROOT / "compositions" / "q-ref.html",
}

EXIT = 0.55  # seconds the card takes to drop back out of frame


def stamp(template: str, question: str, duration: float) -> str:
    """Swap the question text and retime the clip, entrance untouched."""
    out = template
    out = re.sub(r'data-duration="[\d.]+"', f'data-duration="{duration:.2f}"', out)
    out = re.sub(
        r'(<span class="text" id="qtext">)\s*.*?\s*(</span>)',  # noqa: E501
        lambda m: f"{m.group(1)}\n              {question}\n            {m.group(2)}",
        out,
        flags=re.S,
    )
    # The exit tween is anchored to the end of the hold, not to the reference
    # card's 14.8s length.
    out = re.sub(
        r'(ease: "power2\.in" \}, )[\d.]+\)',
        lambda m: f"{m.group(1)}{duration - EXIT:.2f})",
        out,
    )
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Stamp question cards from the reference card")
    ap.add_argument("plan", type=Path, help="final_cut.json with placed cards")
    args = ap.parse_args()

    templates = {k: p.read_text() for k, p in TEMPLATES.items()}
    cards = json.loads(args.plan.read_text()).get("cards", [])
    if not cards:
        raise SystemExit(f"{args.plan} has no cards")

    for card in cards:
        name = Path(card["asset"]).stem
        kind = card.get("kind", "q")
        duration = card["out_end"] - card["out_start"]
        (OUT_DIR / f"{name}.html").write_text(stamp(templates[kind], card["q"], duration))
        print(f"  {name}.html  {kind:3}  {duration:.2f}s  {card['q']}")
    print(f"wrote {len(cards)} cards to {OUT_DIR}")


if __name__ == "__main__":
    main()
