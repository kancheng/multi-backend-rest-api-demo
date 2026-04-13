# -*- coding: utf-8 -*-
"""Generate resources/views/pantry.blade.php from Flask template (UTF-8 safe)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
SRC = REPO / "flask-app" / "templates" / "index.html"
DST = ROOT / "resources" / "views" / "pantry.blade.php"


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    text = text.replace("Smart Pantry · Flask", "Smart Pantry · Laravel")
    text = text.replace("Flask · Smart Pantry", "Laravel · Smart Pantry")
    text = text.replace(
        '<meta charset="UTF-8">',
        '<meta charset="UTF-8">\n'
        '    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">',
        1,
    )
    text = text.replace("@media (max-width:", "@@media (max-width:", 1)
    text = text.replace(
        "'<td>' + escapeHtml(item.expiry_date) + '</td>' +",
        "'<td>' + escapeHtml(formatDateOnly(item.expiry_date)) + '</td>' +",
    )
    insert = """
    function formatDateOnly(v) {
        const s = String(v);
        return s.length >= 10 ? s.slice(0, 10) : s;
    }

"""
    needle = "    function renderRow(item) {"
    if "function formatDateOnly" not in text:
        text = text.replace(needle, insert + needle, 1)
    text = text.replace(
        "document.getElementById('f-exp').value = item.expiry_date;",
        "document.getElementById('f-exp').value = formatDateOnly(item.expiry_date);",
    )
    DST.write_text(text, encoding="utf-8")
    print("Wrote", DST)


if __name__ == "__main__":
    main()
