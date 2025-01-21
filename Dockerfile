# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /FreelanceFlow

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    nodejs \
    npm \
    redis \
    supervisor && \
    apt-get clean

# Copy and install root-level Node.js dependencies
COPY package.json package-lock.json* /FreelanceFlow/
RUN npm install

# Copy and install inner-directory Node.js dependencies
COPY FreelanceFlow/package.json FreelanceFlow/package-lock.json* /FreelanceFlow/FreelanceFlow/
RUN cd FreelanceFlow && npm install

# Copy Python dependencies and install
COPY requirements.txt /FreelanceFlow/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . /FreelanceFlow/

# Copy the supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the application port
EXPOSE 8000

# Run supervisord
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
