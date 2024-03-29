# Use an official Python runtime as a parent image
FROM python:3.7

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application into the container
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV PORT 8080

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]