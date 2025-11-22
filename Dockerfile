# Python 3.11 Slim Image usage
FROM python:3.11-slim

# Set working directory for the application
WORKDIR /app

# Copy requirements file in order to install dependencies
COPY app/requirements.txt .

# Install dependencies based on requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app/ .

# Use port 31415 for the application
EXPOSE 31415

# Run the Flask application
CMD ["python", "app.py"]
