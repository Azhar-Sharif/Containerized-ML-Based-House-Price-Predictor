
# Use the official Python image as a base
FROM python:3.8

# Set the working directory in the container
WORKDIR /multi_container_app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose the port that the app runs on
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=ML_application.py

# Run the application
ENTRYPOINT ["flask", "run", "--host=0.0.0.0","--port=5000"]
