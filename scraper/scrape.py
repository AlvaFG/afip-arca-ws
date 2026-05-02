"""
AFIP/ARCA Web Services documentation scraper.

Crawls https://www.afip.gob.ar/ws/ recursively and converts each page
to clean Markdown with frontmatter. Output goes to ../docs/.

Usage:
    python scrape.py                    # full crawl using config.yaml
    python scrape.py --url <URL>        # scrape a single page
    python scrape.py --max-pages 10     # limit for testing
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
import yaml
from markdownify import markdownify as md
from selectolax.parser import HTMLParser

DEFAULT_CONFIG = Path(__file__).parent / "config.yaml"


class DocsScraper:
    def __init__(self, config: dict):
        self.base_url: str = config["base_url"].rstrip("/")
        self.allowed_prefix: str = config.get("allowed_prefix", self.base_url)
        self.output_dir = Path(config.get("output_dir", "../docs")).resolve()
        self.content_selector: str = config.get("content_selector", "main")
        self.exclude_patterns: list[str] = config.get("exclude_patterns", [])
        self.include_extensions: tuple[str, ...] = tuple(
            config.get("include_extensions", [".asp", ".html", ".htm", "/"])
        )
        self.delay: float = float(config.get("delay_seconds", 0.6))
        self.max_pages: int = int(config.get("max_pages", 1000))
        self.start_urls: list[str] = config.get("start_urls") or [self.base_url + "/"]

        self.visited: set[str] = set()
        self.client = httpx.Client(
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (compatible; DocsScraper/1.0; "
                    "+https://github.com/AlvaFG/afip-arca-ws)"
                ),
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "es-AR,es;q=0.9",
            },
            follow_redirects=True,
            timeout=30.0,
        )

    # ---------- fetching ----------
    def fetch(self, url: str) -> str | None:
        try:
            resp = self.client.get(url)
            resp.raise_for_status()
            ctype = resp.headers.get("content-type", "")
            if "html" not in ctype:
                print(f"  ⏭  skip non-html ({ctype})")
                return None
            return resp.text
        except httpx.HTTPError as e:
            print(f"  ❌ {type(e).__name__}: {e}")
            return None

    # ---------- link discovery ----------
    def is_internal_doc_link(self, url: str) -> bool:
        if not url.startswith(self.allowed_prefix):
            return False
        if any(re.search(pat, url) for pat in self.exclude_patterns):
            return False
        path = urlparse(url).path.lower()
        return path.endswith(self.include_extensions) or path.endswith("/")

    def discover_links(self, html: str, current_url: str) -> list[str]:
        tree = HTMLParser(html)
        links: list[str] = []
        for node in tree.css("a[href]"):
            href = node.attributes.get("href", "").strip()
            if not href or href.startswith(("#", "mailto:", "javascript:", "tel:")):
                continue
            absolute = urljoin(current_url, href).split("#")[0]
            if self.is_internal_doc_link(absolute) and absolute not in links:
                links.append(absolute)
        return links

    # ---------- content extraction ----------
    def extract_content(self, html: str) -> tuple[str, str]:
        tree = HTMLParser(html)

        # title
        title_node = tree.css_first("h1") or tree.css_first("title")
        title = title_node.text(strip=True) if title_node else "Untitled"
        # AFIP often appends "| ARCA" — strip it
        title = re.sub(r"\s*[|·]\s*ARCA\s*$", "", title, flags=re.I)

        # main content — try several selectors
        content = None
        for selector in [self.content_selector, "main", "#content", "article", ".contenido", "body"]:
            node = tree.css_first(selector)
            if node and len(node.text(strip=True)) > 100:
                content = node
                break
        if content is None:
            return title, ""

        # strip noise
        for sel in ["script", "style", "nav", "header", "footer",
                    ".sidebar", ".breadcrumb", ".menu", "#menu", ".redes-sociales"]:
            for noise in content.css(sel):
                noise.decompose()

        markdown = md(content.html or "", heading_style="ATX", bullets="-", strip=["img"])
        markdown = re.sub(r"\n{3,}", "\n\n", markdown)
        markdown = re.sub(r"[ \t]+\n", "\n", markdown)
        return title, markdown.strip()

    # ---------- file output ----------
    def url_to_path(self, url: str) -> Path:
        path = urlparse(url).path
        # strip prefix common to all docs
        prefix = urlparse(self.base_url).path.rstrip("/")
        if path.startswith(prefix):
            path = path[len(prefix):]
        path = path.strip("/") or "index"
        # turn .asp into .md
        path = re.sub(r"\.(asp|html?|php)$", "", path, flags=re.I)
        if path.endswith("/"):
            path += "index"
        return self.output_dir / f"{path}.md"

    # ---------- main loop ----------
    def scrape(self, start_urls: list[str] | None = None) -> dict:
        queue: list[str] = list(start_urls) if start_urls else list(self.start_urls)
        stats = {"pages": 0, "errors": 0, "skipped": 0}
        index_entries: list[tuple[str, str]] = []

        while queue and stats["pages"] < self.max_pages:
            url = queue.pop(0)
            if url in self.visited:
                continue
            self.visited.add(url)

            print(f"[{stats['pages']+1:>3}] {url}")
            html = self.fetch(url)
            if html is None:
                stats["errors"] += 1
                continue

            title, markdown = self.extract_content(html)
            if not markdown or len(markdown) < 50:
                print("  ⏭  empty/too-short content")
                stats["skipped"] += 1
            else:
                out = self.url_to_path(url)
                out.parent.mkdir(parents=True, exist_ok=True)
                frontmatter = (
                    f"---\n"
                    f'source_url: "{url}"\n'
                    f'title: "{title.replace(chr(34), chr(39))}"\n'
                    f"scraped_at: {time.strftime('%Y-%m-%d')}\n"
                    f"---\n\n"
                )
                out.write_text(frontmatter + f"# {title}\n\n{markdown}\n", encoding="utf-8")
                rel = out.relative_to(self.output_dir).as_posix()
                index_entries.append((title, rel))
                stats["pages"] += 1
                print(f"  ✅ {rel}")

            for link in self.discover_links(html, url):
                if link not in self.visited:
                    queue.append(link)

            time.sleep(self.delay)

        self._write_index(index_entries)
        return stats

    def _write_index(self, entries: list[tuple[str, str]]):
        if not entries:
            return
        lines = [
            "# AFIP/ARCA Web Services — Documentation Index",
            "",
            f"_Auto-generated from {self.base_url}_  ",
            f"_Last update: {time.strftime('%Y-%m-%d')}_",
            "",
            f"**Total pages:** {len(entries)}",
            "",
            "## Pages",
            "",
        ]
        for title, path in sorted(entries, key=lambda x: x[1]):
            lines.append(f"- [{title}]({path})")
        # write to README.md (not index.md) to avoid clashing with a scraped page
        # whose URL maps to docs/index.md
        (self.output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_config(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Scrape AFIP WS docs to Markdown")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--url", type=str, help="Start from this URL only")
    parser.add_argument("--max-pages", type=int, help="Override max_pages")
    args = parser.parse_args()

    config = load_config(args.config)
    if args.max_pages:
        config["max_pages"] = args.max_pages

    scraper = DocsScraper(config)
    start = [args.url] if args.url else None
    stats = scraper.scrape(start)

    print("\n" + "=" * 50)
    print(f"✅ Pages scraped: {stats['pages']}")
    print(f"⏭  Skipped:       {stats['skipped']}")
    print(f"❌ Errors:        {stats['errors']}")
    print(f"📁 Output:        {scraper.output_dir}")
    return 0 if stats["pages"] > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
