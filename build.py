#!/usr/bin/env python3
"""Собирает _site/index.html из links.yaml и template.html."""
import html
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).parent
OUT = ROOT / "_site"


def esc(s):
    return html.escape(str(s or "").strip(), quote=True)


def render_link(link):
    title = esc(link["title"])
    url = esc(link["url"])
    desc = esc(link.get("description"))
    desc_html = f'<span class="desc">{desc}</span>' if desc else ""
    return (
        f'<a class="link" href="{url}" target="_blank" rel="noopener">'
        f'<span class="title">{title}</span>{desc_html}</a>'
    )


def render(data):
    parts = []
    for block in data:
        section = esc(block.get("section"))
        closed = " closed" if block.get("section") == "Закрыто" else ""
        items = "\n".join(render_link(l) for l in block.get("links") or [])
        heading = f"<h2>{section}</h2>" if section else ""
        parts.append(f'<section class="group{closed}">{heading}\n{items}\n</section>')
    return "\n".join(parts)


def main():
    data = yaml.safe_load((ROOT / "links.yaml").read_text(encoding="utf-8"))
    for block in data:
        for l in block.get("links") or []:
            assert l.get("title") and l.get("url"), f"title и url обязательны: {l}"
    template = (ROOT / "template.html").read_text(encoding="utf-8")
    page = template.replace("{{ links }}", render(data))

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / "index.html").write_text(page, encoding="utf-8")
    shutil.copytree(ROOT / "assets", OUT / "assets")
    shutil.copy(ROOT / "CNAME", OUT / "CNAME")
    print(f"OK: {sum(len(b.get('links') or []) for b in data)} ссылок → {OUT / 'index.html'}")


if __name__ == "__main__":
    main()
