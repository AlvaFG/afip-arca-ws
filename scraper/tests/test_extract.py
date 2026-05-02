from pathlib import Path

import pytest

from scrape import DocsScraper

FIXTURE = Path(__file__).parent / "fixtures" / "sample_page.html"


@pytest.fixture
def scraper(tmp_path):
    return DocsScraper({
        "base_url": "https://www.afip.gob.ar/ws",
        "allowed_prefix": "https://www.afip.gob.ar/ws",
        "output_dir": str(tmp_path),
        "content_selector": "main",
        "delay_seconds": 0,
        "max_pages": 10,
    })


def test_extract_strips_arca_suffix_from_title(scraper):
    html = FIXTURE.read_text(encoding="utf-8")
    title, _ = scraper.extract_content(html)
    assert title == "WSAA - Web Service de Autenticación"


def test_extract_keeps_table_content(scraper):
    html = FIXTURE.read_text(encoding="utf-8")
    _, md = scraper.extract_content(html)
    assert "Homologación" in md
    assert "wsaahomo.afip.gov.ar" in md


def test_extract_strips_nav_and_footer(scraper):
    html = FIXTURE.read_text(encoding="utf-8")
    _, md = scraper.extract_content(html)
    assert "menu noise" not in md
    assert "footer noise" not in md


def test_url_to_path_converts_asp_to_md(scraper, tmp_path):
    p = scraper.url_to_path("https://www.afip.gob.ar/ws/programadores/certificados-digitales.asp")
    assert p == tmp_path / "programadores" / "certificados-digitales.md"


def test_url_to_path_handles_root(scraper, tmp_path):
    p = scraper.url_to_path("https://www.afip.gob.ar/ws/")
    assert p == tmp_path / "index.md"


def test_discover_links_separates_docs_and_assets(scraper):
    html = FIXTURE.read_text(encoding="utf-8")
    docs, assets = scraper.discover_links(html, "https://www.afip.gob.ar/ws/")
    assert "https://www.afip.gob.ar/ws/programadores/certificados-digitales.asp" in docs
    assert "https://www.afip.gob.ar/ws/documentacion/wsaa-manual.pdf" in assets
