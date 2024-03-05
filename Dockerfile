# Use the official Python image as base
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the application files into the container
COPY . .

# Upgrade pip to ensure the latest version is used
RUN pip install --upgrade pip

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port used by the application (if applicable)
# EXPOSE 8050

# Define the command to run the application
CMD ["python", "ena-CLI"]
