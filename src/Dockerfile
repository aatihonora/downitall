FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /downitall
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libffi-dev \
    libssl-dev \
    mpv \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip-related tools
RUN pip install --upgrade pip setuptools wheel
COPY . .
# Install dependencies
RUN pip install .
RUN apt-get update && apt-get install -y python3 chromium chromium-driver git aria2 wget && rm -rf /var/lib/apt/lists/* 
CMD ["downitall"]
