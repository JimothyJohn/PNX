FROM python:3.11-slim-bookworm

# Configure environment
ENV DEBIAN_FRONTEND=noninteractive \
    PIP_PREFER_BINARY=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install --no-cache-dir -U poetry

# Create the /pnx directory and change ownership to appuser
RUN mkdir -p /pnx && \
    useradd -m appuser && \
    chown -R appuser:appuser /pnx
# Copy the pyproject.toml into the working directory
COPY pyproject.toml /pnx/ 

# Set the working directory to /pnx
WORKDIR /pnx

# Switch to the appuser
USER appuser

# Install dependencies using Poetry
RUN poetry install

# Set entrypoint or command if needed
CMD ["poetry", "install"]
