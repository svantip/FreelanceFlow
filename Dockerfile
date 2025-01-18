# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /FreelanceFlow

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev nodejs npm supervisor

# Copy and install root-level Node.js dependencies
COPY package.json package-lock.json* /FreelanceFlow/
RUN npm install

# Copy and install inner-directory Node.js dependencies
COPY FreelanceFlow/package.json FreelanceFlow/package-lock.json* /FreelanceFlow/FreelanceFlow/
RUN cd FreelanceFlow && npm install

# Copy Python dependencies first (leverage Docker cache)
COPY requirements.txt /FreelanceFlow/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . /FreelanceFlow/

# Copy the supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the port the app will run on
EXPOSE 8000

# Run supervisord
CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]