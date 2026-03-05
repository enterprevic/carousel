FROM python:3.12-slim AS base

WORKDIR /app

# System deps for Playwright — cached as a separate layer
RUN apt-get update && apt-get install -y \
    wget gnupg curl \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libasound2 libpango-1.0-0 libcairo2 libxshmfence1 \
    fonts-liberation fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

# Install playwright package alone first so browser download is cached independently
RUN pip install --no-cache-dir playwright==1.49.0
RUN playwright install chromium

# Now install the rest of the dependencies (changes here won't bust the Chromium layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
