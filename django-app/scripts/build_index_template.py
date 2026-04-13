# -*- coding: utf-8 -*-
"""Write templates/index.html from Flask template (UTF-8). Fixes CP1252/mojibake in title."""
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "flask-app" / "templates" / "index.html"
DST = REPO / "django-app" / "templates" / "index.html"


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    text = text.replace("Smart Pantry · Flask", "Smart Pantry · Django")
    text = text.replace("Flask · Smart Pantry", "Django · Smart Pantry")
    DST.write_text(text, encoding="utf-8", newline="\n")
    print("Wrote", DST)


if __name__ == "__main__":
    main()
