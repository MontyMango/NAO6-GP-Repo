# Use an official Python runtime
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port 45689
EXPOSE 45689

# Run the application
CMD ["python3", "mySpeechRecognition.py"]

