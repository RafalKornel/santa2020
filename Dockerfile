# Use the official Python 3.8 image as a base
FROM python:3.8-slim

# Set environment variables to prevent Python from generating .pyc files and to buffer output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install system dependencies (for psycopg2 and other packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the application code into the container
COPY . /app/

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the Gunicorn server (matches the Procfile `web` entry)
CMD ["gunicorn", "wsgi:app", "--log-file", "-", "--bind" "0.0.0.0:8000"]
