# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variable to prevent buffering
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn watchdog daphne

# Copy the rest of the application code to /app
COPY . /app/

# Copy the entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

# Command to run the script
CMD ["watchmedo", "auto-restart", "--directory=.", "--pattern=*.py;*.html", "--recursive", "--", "daphne", "-b", "0.0.0.0", "-p", "8000", "DjangoLiveStreaming.asgi:application"]
