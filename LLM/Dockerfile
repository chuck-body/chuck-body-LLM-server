FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3-pip \
	ffmpeg \
	flac \
    openjdk-17-jre-headless \
    build-essential \
    && pip3 install --upgrade pip

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    flac \
	openjdk-11-jre \
    && rm -rf /var/lib/apt/lists/*
# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 