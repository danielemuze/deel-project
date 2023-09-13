# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory
WORKDIR /app

# Install Flask and psycopg2
RUN pip install Flask psycopg2-binary

# Copy the current directory contents into the container
COPY . /app/

# Run app.py when the container launches
CMD ["python", "app.py"]