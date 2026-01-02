FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libnspr4 \
    libnss3 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    fonts-liberation \
    ca-certificates \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .


RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt    

#for cpu that does not support x86-64v2 baseline optimization
RUN pip uninstall -y numpy && \
    pip install numpy==1.26.4

RUN playwright install-deps
RUN playwright install

COPY . .

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

CMD ["python", "app.py"]
