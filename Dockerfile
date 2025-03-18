# Use official Python image
FROM python:3.12.8

# Set the working directory inside the container
WORKDIR /app

# Copy the Flask app code to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port (5000)
EXPOSE 5000

# Run the Flask app
CMD ["python", "server.py"]