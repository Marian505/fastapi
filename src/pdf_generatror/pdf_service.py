import asyncio
import logging
import os
from dotenv import load_dotenv
from pyppeteer import launch


load_dotenv()
logger = logging.getLogger(__name__)
IS_LOCAL = os.getenv("ENVIRONMENT", "local") == "local"
BROWSER_PATH = os.getenv("PUPPETEER_EXECUTABLE_PATH")

_browser = None
_browser_lock = None

async def get_browser():
    """Get or create browser instance."""
    global _browser, _browser_lock
    
    if _browser_lock is None:
        _browser_lock = asyncio.Lock()
    
    async with _browser_lock:
        if _browser is not None:
            return _browser
        
        try:
            if IS_LOCAL and BROWSER_PATH:
                logger.info(f"Local mode: Launching browser from {BROWSER_PATH}")
                _browser = await launch(
                    executablePath=BROWSER_PATH,
                    headless=True,
                    args=["--no-sandbox", "--disable-gpu"]
                )
            else:
                logger.info("Production mode: Auto-detecting browser")
                _browser = await launch(
                    headless=True,
                    args=["--no-sandbox", "--disable-gpu"]
                )
            
            logger.info("Browser launched successfully")
            return _browser
            
        except Exception as e:
            logger.error(f"Failed to launch browser: {e}")
            raise

async def close_browser():
    global _browser
    async with _browser_lock:
        if _browser is not None:
            await _browser.close()
            _browser = None

async def generate_pdf_from_html(html_content: str) -> bytes:
    try:
        browser = await get_browser()
        page = await browser.newPage()
        await page.setContent(html_content)
        pdf_bytes = await page.pdf({'format': 'A4', 'margin': {'top': '10mm', 'bottom': '10mm'}})
        
        return pdf_bytes
    except Exception as e:
        logger.error(f"PDF generation failed: {e}")
        return f"Error: {str(e)}"
    finally:
        if page is not None:
            await page.close()