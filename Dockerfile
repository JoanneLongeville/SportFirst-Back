# Use the latest Python base image. If space is an issue, use python:3.12-slim
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container's working directory
COPY . /app

# Upgrade setuptools, pip, and wheel
RUN pip install --upgrade setuptools pip wheel

# Install the application dependencies with pip
RUN pip install -v --no-cache-dir -r requirements.txt

# Expose the port used by the application
EXPOSE 5000

# Default command to run when the container starts
CMD ["python", "app/src/main.py"]

