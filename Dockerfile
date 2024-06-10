# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY req.txt .

# Install dependencies
RUN pip install -r req.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose the port that the FastAPI application will run on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
