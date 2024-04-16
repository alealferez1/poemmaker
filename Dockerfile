# Use a lightweight Python base image
FROM python:3.9-slim 

# Define a working directory within the container
WORKDIR /app

# Copy requirements.txt first for efficient caching
COPY requirements.txt ./requirements.txt

# Install the required dependencies
RUN pip install -r requirements.txt 

# Copy the rest of your application code
COPY . .  

# Specify the command to execute when the container starts
CMD ["python", "app.py"]