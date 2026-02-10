FROM python:3.14-slim

RUN pip install --no-cache-dir uv

RUN apt-get update && apt-get install -y \
    chromium

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium \
    PUPPETEER_DISABLE_DEV_SHM_USAGE=true

WORKDIR /app

COPY . .

RUN uv sync --no-install-project --no-dev

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
