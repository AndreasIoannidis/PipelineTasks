# Use a slim Python 3.12 image as the build stage base.
FROM python:3.12-slim AS builder

# Work in a dedicated directory while installing dependencies.
WORKDIR /build

# Copy only the dependency list so this layer can be cached.
COPY requirements.txt .

# Install packages into /install so they can be copied without pip in the final image.
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Start a clean runtime image without build tools or pip caches.
FROM python:3.12-slim

# Create a non-root user that will run the application.
RUN useradd --create-home --uid 1000 appuser

# Set the working directory for the copied application.
WORKDIR /app

# Copy the installed packages from the builder into the system prefix.
COPY --from=builder /install /usr/local

# Copy only the application package into the image.
COPY app ./app

# Drop privileges and run the process as the non-root user.
USER appuser

# Document that the API listens on port 8000.
EXPOSE 8000

# Start uvicorn and bind to all interfaces so the container is reachable.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
