# Use a base image with Python
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt file into the container
COPY requirements.txt requirements.txt

# Install the necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Expose the port on which the app will run
EXPOSE 5000

# Set the entry point to run the app
CMD ["python", "app.py"]
