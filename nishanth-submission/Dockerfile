# Uses an official Python runtime as the base image
FROM python:3.9-slim

# Sets the working directory in the container
WORKDIR /app

# Copies the requirements file into the container
COPY requirements.txt .

# Installs the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copies the project files into the container
COPY . .

# Sets environment variables
ENV PYTHONUNBUFFERED=1

# Creates necessary directories
RUN mkdir -p data/raw data/processed data/anonymized

# Sets the entrypoint to Python
ENTRYPOINT ["python"]

# Default command
CMD ["src/data_generator.py", "personal_info"]