# # Use the official Python image
# FROM python:3.10-slim

# # Set the working directory inside the container
# WORKDIR /app

# # Copy project files into the container
# COPY . /app

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Default command to run Celery worker
# CMD ["celery", "-A", "tasks", "worker", "--pool=threads", "--loglevel=info"]

# Use a base image with Python 3.10 or higher
FROM python:3.10-bullseye

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file into the container
COPY requirements.txt /app/

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y openjdk-11-jre-headless && \
    rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Copy the rest of the application code
COPY . /app/

# Expose the port your Flask app runs on
EXPOSE 5000

# Command to run the Flask application
CMD ["flask", "-app app", "run", "--host 0.0.0.0"]
