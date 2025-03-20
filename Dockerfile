# Use official Python image
FROM python:3.12.8

# Set the working directory inside the container
WORKDIR /app

# Copy the Flask app code to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port (5001)
EXPOSE 5001

# Run the Flask app
CMD ["python", "server.py"]