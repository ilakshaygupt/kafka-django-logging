# Use the official Python image as a base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django app
COPY . /app/

# Expose the Django port
EXPOSE 8000

# Start Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
