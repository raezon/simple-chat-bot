# Use an official TensorFlow runtime as a parent image
# FROM tensorflow/tensorflow:latest

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install project dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the port for the Flask application
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]
