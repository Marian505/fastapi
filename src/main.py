from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.pdf_generatror.pdf_controller import router
from src.pdf_generatror.pdf_service import close_browser

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic (optional)
    yield
    # Shutdown logic
    await close_browser()

app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix="/api")

