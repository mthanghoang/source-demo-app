# Use a minimal base image with Python 3
FROM python:3.10-alpine

# Set working directory
WORKDIR /usr/src/app

# Install build dependencies (if needed by Python packages)
# && clean up to reduce image size
RUN apk add --no-cache --virtual .build-deps && \
    pip install --upgrade pip

# Copy only requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies without caching
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Remove build dependencies to reduce final image size
RUN apk del .build-deps

# Expose the app port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
