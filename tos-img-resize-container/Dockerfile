FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and run script
COPY index.py .
COPY start.sh .

# Make run.sh executable
RUN chmod +x start.sh

# Expose port (Flask default)
EXPOSE 8080

# Set entrypoint to run.sh for BytePlus Function Service
ENTRYPOINT ["./run.sh"]