from fastapi.testclient import TestClient
from src.main import app
from src.pdf_generatror import pdf_controller

client = TestClient(app)

def test_get_ok():
    response = client.get("/api/ok")
    assert response.status_code == 200
    assert response.text == '"OK"'


def test_html_to_pdf_returns_base64(monkeypatch):
    async def fake_generate(html: str) -> bytes:
        assert html == "hello"
        return b"pdf"

    monkeypatch.setattr(pdf_controller, "generate_pdf_from_html", fake_generate)

    response = client.post(
        "/api/html-to-pdf",
        content="hello",
        headers={"Content-Type": "text/plain"},
    )

    assert response.status_code == 200
    assert response.json()["pdf_base64"] == "cGRm"


def test_html_to_pdf_streaming_returns_pdf(monkeypatch):
    async def fake_generate(html: str) -> bytes:
        assert html == "hello"
        return b"pdf"

    monkeypatch.setattr(pdf_controller, "generate_pdf_from_html", fake_generate)

    response = client.post(
        "/api/html-to-pdf-streaming",
        content="hello",
        headers={"Content-Type": "text/plain"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/pdf")
    assert response.headers["content-disposition"] == "attachment; filename=generated.pdf"
    assert response.content == b"pdf"