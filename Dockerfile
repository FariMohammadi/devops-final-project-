# Base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy and install dependencies first (for faster rebuilds)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY app/ .

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]