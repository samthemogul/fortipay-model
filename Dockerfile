FROM python:3.12  

# Install OpenGL for OpenCV
RUN apt-get update && apt-get install -y libgl1

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app/

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
