# Use an official Python runtime as a parent image
FROM python:3.10

# Install system dependencies required by psycopg2 (PostgreSQL adapter)
RUN apt-get update && apt-get install -y \
    gcc libpq-dev && \
    # Clean up apt cache to reduce image size \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file first to leverage Docker cache
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
# (files specified in .dockerignore will be excluded)
COPY . .

# Make port 5000 available to the world outside this container
# This is good practice for documentation, but the actual mapping is in docker-compose.yml
EXPOSE 5000

# Run the app.
# --host=0.0.0.0 makes the server accessible from outside the container.
# --reload automatically reloads the server on code changes (for development).
CMD ["flask", "run", "--host=0.0.0.0", "--reload"]
