# Use a lightweight Python image
FROM python:3.11-slim

# Install system dependencies required by Playwright
RUN apt-get update && apt-get install -y \
    wget gnupg ca-certificates fonts-liberation libasound2 libatk1.0-0 \
    libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 \
    libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy everything to /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers *inside* the Docker image
RUN python -m playwright install --with-deps chromium

# Set environment variables for Playwright runtime
ENV PLAYWRIGHT_BROWSERS_PATH=/root/.cache/ms-playwright
ENV PYTHONUNBUFFERED=1

# Expose Render's port
EXPOSE 10000

# Start Flask app using Gunicorn
CMD ["gunicorn", "basic:app", "--bind", "0.0.0.0:10000"]
