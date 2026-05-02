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


def test_extract_preserves_table_as_markdown_pipe_table(scraper):
    html = FIXTURE.read_text(encoding="utf-8")
    _, md = scraper.extract_content(html)
    assert "|" in md
    assert "Ambiente" in md and "URL" in md


def test_assets_index_is_sorted_and_writes_file(scraper, tmp_path):
    assets = [
        "https://www.afip.gob.ar/ws/z.wsdl",
        "https://www.afip.gob.ar/ws/a.pdf",
        "https://www.afip.gob.ar/ws/m.xsd",
    ]
    scraper._write_assets_index(sorted(assets))
    out = (tmp_path / "_assets-index.md").read_text(encoding="utf-8")
    a_pos = out.index("a.pdf")
    m_pos = out.index("m.xsd")
    z_pos = out.index("z.wsdl")
    assert a_pos < m_pos < z_pos


def test_index_is_written_even_with_no_pages(scraper, tmp_path):
    scraper._write_index([])
    readme = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "No pages were scraped" in readme
