# Dockerfile

# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy all source code into the container
COPY . .

# Make the entrypoint script executable (important for cross-platform use)
RUN chmod +x entrypoint.sh

# Install Python dependencies without cache
RUN pip install --no-cache-dir -r requirements.txt

# Default command when the container starts
ENTRYPOINT ["bash", "entrypoint.sh"]
