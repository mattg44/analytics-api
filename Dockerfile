FROM python:3.13-slim

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install os dependencies for our mini vm
RUN apt-get update && apt-get install -y \
    # for postgres
    libpq-dev \
    # for Pillow
    libjpeg-dev \
    # for CairoSVG
    libcairo2 \
    # other
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to that same code directory
WORKDIR /code

# Copy the application into the container.
COPY . /code

# Make the startup script executable
RUN chmod +x /code/start.sh

# Install the application dependencies.
RUN uv sync --frozen --no-cache

# Run the application.
CMD ["/code/start.sh"]