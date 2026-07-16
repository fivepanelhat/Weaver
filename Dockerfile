FROM python:3.10-slim

# Install system dependencies including git for git-based pip requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
 build-essential \
 git \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set default command - runs the multi-tenant helpdesk demo (offline-capable).
# Weaver is a library/orchestrator, not a long-running server; override this
# CMD to run your own entrypoint against the orchestrator API.
CMD ["python", "demo.py"]
