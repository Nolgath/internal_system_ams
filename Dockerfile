# Use lightweight Python image
FROM python:3.11-slim

# Install Linux libraries required by Playwright
RUN apt-get update && apt-get install -y \
    wget gnupg ca-certificates fonts-liberation libasound2 libatk1.0-0 \
    libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 \
    libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 xdg-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# --- Key change here ---
# Force Playwright to install Chromium into /app/ms-playwright (baked into final image)
ENV PLAYWRIGHT_BROWSERS_PATH=/app/ms-playwright
RUN python -m playwright install --with-deps chromium

# Make sure Playwright knows where the binary lives
ENV PATH="/app/ms-playwright/chromium-*/chrome-linux:${PATH}"
ENV PYTHONUNBUFFERED=1

EXPOSE 10000
CMD ["gunicorn", "basic:app", "--bind", "0.0.0.0:10000"]
