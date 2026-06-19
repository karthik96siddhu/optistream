# =========================================================
# STAGE 1: The Builder (Heavy environment to compile tools)
# =========================================================
FROM python:3.11-slim AS builder

# Prevent Python from writing .pyc files to disk (saves space/noise)
ENV PYTHONDONTWRITEBYTECODE=1
# Force stdout and stderr streams to be unbuffered (ensures logs appear instantly)
ENV PYTHONUNBUFFERED=1

WORKDIR /build

# Install basic OS compilation tools needed for installing dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy just the requirements file first to take advantage of Docker caching
COPY requirements.txt .

# Install dependencies into a localized wheelhouse folder
RUN pip install --no-cache-dir --user -r requirements.txt


# =========================================================
# STAGE 2: The Final Production Runner (Minimalist & Secure)
# =========================================================
FROM python:3.11-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Create a security-focused, low-privilege system group and user
RUN groupadd -r appgroup && useradd -r -g appgroup -s /sbin/nologin appuser

# 2. Copy the installed Python dependencies from Stage 1 (Builder)
COPY --from=builder /root/.local /home/appuser/.local
COPY --from=builder /build /app

# Ensure our new low-privilege user can access the installed packages
ENV PATH=/home/appuser/.local/bin:$PATH

# 3. Create a temporary folder for our PDF background processing
RUN mkdir -p /app/tmp/invoices && chown -R appuser:appgroup /app

# 4. Switch from 'root' to our secured, non-root system user
USER appuser

# 5. Copy the actual application source code into the runner
COPY ./app /app/app

# Expose port 8000 so the network knows where our FastAPI app listens
EXPOSE 8000

# Command to spin up our production web server using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]