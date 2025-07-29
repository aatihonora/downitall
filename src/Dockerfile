FROM python:3.12-slim

# Set working directory inside the container.
WORKDIR /downitall
# Installing develop dependencies.
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip-related tools
RUN pip install --upgrade pip setuptools wheel
# Getting all files.
COPY . .
# Install dependencies.
RUN pip install .
# Installing external dependencies.
RUN apt-get update && apt-get install -y python3 chromium chromium-driver git mpv aria2 wget && rm -rf /var/lib/apt/lists/* 
# Running the app.
CMD ["downitall"]
