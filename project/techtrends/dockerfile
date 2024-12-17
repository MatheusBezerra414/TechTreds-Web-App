# Use Python 3.8 base image
FROM python:3.8

# Set environment variables to prevent buffering
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Initialize the database
RUN python init_db.py

# Expose port 3111 for the application
EXPOSE 3111

# Define the command to run the application
CMD ["python", "app.py"]