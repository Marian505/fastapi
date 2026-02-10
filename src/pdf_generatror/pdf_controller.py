from io import BytesIO
from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from src.pdf_generatror.pdf_service import generate_pdf_from_html
import base64
router = APIRouter()

@router.get("/ok")
async def get_ok() -> str:
    return "OK"

@router.post("/html-to-pdf")
async def html_to_pdf(html: str = Body(..., media_type='text/plain')) -> dict[str, str]:

    pdf_bytes = await generate_pdf_from_html(html)
    content= base64.b64encode(pdf_bytes).decode('ascii')

    return {"pdf_base64": content}


@router.post("/html-to-pdf-streaming")
async def html_to_pdf_streaming(html: str = Body(..., media_type='text/plain')) -> StreamingResponse:

    pdf_bytes = await generate_pdf_from_html(html)

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=generated.pdf"}
    )
