import asyncio

from src.pdf_generatror import pdf_service as svc


class FakePage:
    def __init__(self):
        self.content = None
        self.pdf_options = None
        self.closed = False

    async def setContent(self, html):
        self.content = html

    async def pdf(self, options):
        self.pdf_options = options
        return b"%PDF-1.4"

    async def close(self):
        self.closed = True


class FakeBrowser:
    def __init__(self, page=None):
        self.page = page or FakePage()
        self.closed = False
        self.new_page_calls = 0

    async def newPage(self):
        self.new_page_calls += 1
        return self.page

    async def close(self):
        self.closed = True


def run(coro):
    return asyncio.run(coro)


def reset_state():
    svc._browser = None
    svc._browser_lock = None


def test_get_browser_uses_executable_path(monkeypatch):
    reset_state()
    fake_browser = FakeBrowser()
    launch_calls = {}

    async def fake_launch(**kwargs):
        launch_calls.update(kwargs)
        return fake_browser

    monkeypatch.setattr(svc, "launch", fake_launch)
    monkeypatch.setattr(svc, "IS_LOCAL", True)
    monkeypatch.setattr(svc, "BROWSER_PATH", "C:/chrome")

    browser = run(svc.get_browser())

    assert browser is fake_browser
    assert launch_calls["executablePath"] == "C:/chrome"
    assert launch_calls["headless"] is True
    assert "--no-sandbox" in launch_calls["args"]


def test_get_browser_returns_cached(monkeypatch):
    reset_state()
    fake_browser = FakeBrowser()
    svc._browser = fake_browser
    svc._browser_lock = asyncio.Lock()

    async def fake_launch(**kwargs):
        raise AssertionError("launch should not be called")

    monkeypatch.setattr(svc, "launch", fake_launch)

    browser = run(svc.get_browser())

    assert browser is fake_browser


def test_generate_pdf_from_html_closes_page(monkeypatch):
    reset_state()
    page = FakePage()
    browser = FakeBrowser(page=page)

    async def fake_get_browser():
        return browser

    monkeypatch.setattr(svc, "get_browser", fake_get_browser)

    result = run(svc.generate_pdf_from_html("<html></html>"))

    assert result == b"%PDF-1.4"
    assert page.closed is True
    assert page.content == "<html></html>"
    assert page.pdf_options["format"] == "A4"


def test_close_browser_closes_and_clears():
    reset_state()
    browser = FakeBrowser()
    svc._browser = browser
    svc._browser_lock = asyncio.Lock()

    run(svc.close_browser())

    assert browser.closed is True
    assert svc._browser is None