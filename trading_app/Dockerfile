# Use the official Python 3 image as the base image
FROM python:3

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the required Python packages
RUN pip install -r requirements.txt

# Copy the rest of the files to the working directory
COPY . .

# Expose port 5672 for RabbitMQ
EXPOSE 5672

# Run the exchange.py script when the container launches
CMD ["python", "exchange.py", "localhost"]
