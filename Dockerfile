# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and other project files into the container
COPY . /app

# Install dependencies
RUN pip install -e .

# Run the application, passing the server address and port as arguments
ENTRYPOINT ["python", "blockcpi"]
