# Use official Python image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the project files
COPY . /app

# Copy the .env file into the container
COPY .env /app/.env

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure Django loads the .env file
RUN pip install django-environ

# Set environment variables inside the image
ENV ENV_FILE_PATH=/app/.env

# Expose the port Django runs on
EXPOSE 8000

# Run Django using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
