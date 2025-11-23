# Use official Python image
FROM python:3.11

# Set work directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project
COPY . .

# Expose port 8000 for Django
EXPOSE 8000

# Load environment variables (from .env)
# NOTE: docker run command will use --env-file to inject this.

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
