# Dockerfile

# Use a modern, slim Python base image
FROM python:3.12-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies needed for compiling Python packages
RUN apt-get update && apt-get install -y \
    # Provides C compilers (gcc) needed for building extensions
    build-essential \
    # Provides the pkg-config tool, required by mysqlclient
    pkg-config \
    # Provides development headers for MySQL, required by mysqlclient
    default-libmysqlclient-dev \
    # Provides the 'mysql' command for testing
    default-mysql-client \
    # Provides development headers for image support (JPEG, PNG), required by Pillow
    libjpeg-dev \
    zlib1g-dev \
    # Clean up apt cache to reduce final image size
    && rm -rf /var/lib/apt/lists/*


# Create a non-root user for security
RUN addgroup --system app && adduser --system --ingroup app appuser

# Set the working directory
WORKDIR /app

# Upgrade pip and install Python dependencies as root
RUN python -m pip install --upgrade pip
COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy the rest of the project files and set ownership
COPY --chown=appuser:app . .

# Switch to the non-root user to run the application
USER appuser