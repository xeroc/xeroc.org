#!/usr/bin/env python3
"""Generate sitemap.xml from built index.html files, stamped with current UTC time.

Run after `make build` compiles the pages. Reads CNAME for the domain so there's
one source of truth. Auto-discovers any **/index.html, so adding a page needs no
edit here.
"""
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CNAME = ROOT / "CNAME"
BASE = "https://" + CNAME.read_text().strip() if CNAME.exists() else "https://xeroc.org"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def loc_for(html: Path) -> str:
    rel = html.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return f"{BASE}/"
    return f"{BASE}/{rel[: -len('index.html')]}"


def is_hidden(html: Path) -> bool:
    return any(part.startswith(".") for part in html.relative_to(ROOT).parts[:-1])


def main() -> None:
    pages = sorted(p for p in ROOT.glob("**/index.html") if not is_hidden(p))
    assert pages, "no index.html found — run the pug build first"

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for p in pages:
        loc = loc_for(p)
        root = loc.rstrip("/") == BASE
        prio, freq = ("1.0", "daily") if root else ("0.8", "weekly")
        lines.append(
            f"  <url><loc>{loc}</loc><lastmod>{NOW}</lastmod>"
            f"<changefreq>{freq}</changefreq><priority>{prio}</priority></url>"
        )
    lines.append("</urlset>")

    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n")
    print(f"sitemap.xml: {len(pages)} url(s) @ {NOW}")


if __name__ == "__main__":
    main()
