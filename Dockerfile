# Use a minimal Python image as the base
FROM python:3.8

# Set the working directory within the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install only essential project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary application code into the container at /app
COPY . /app/

# Define the command to run your application
CMD ["python", "manage.py"]
