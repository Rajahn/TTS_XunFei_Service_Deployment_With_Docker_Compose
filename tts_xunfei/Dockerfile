# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in container to /app
WORKDIR /app

# Copy the current directory contents (where Dockerfile is located) into the container at /app
COPY ./requirements.txt /app/requirements.txt
COPY ./tts_xunfei.py /app/tts_xunfei.py

# Install required packages using pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 5000 for Flask app to listen on
EXPOSE 5000

# Define environment variable
ENV NAME tts_xunfei

# Run tts_xunfei.py when the container launches
CMD ["python", "tts_xunfei.py"]
