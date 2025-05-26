# Use official Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application files
COPY . sql_generator

# Expose port 9000 for FastAPI
EXPOSE 9000

# Start FastAPI server using Uvicorn
# TODO: Replace uvicorn with a production grade ASGI server
CMD python -m src.app.main
