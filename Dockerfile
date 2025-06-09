# Use Python base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all remaining source code into container
COPY . .

# Expose only Streamlit's port
EXPOSE 8501

# Run Streamlit only (the UI)
CMD ["streamlit", "run", "app/ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
