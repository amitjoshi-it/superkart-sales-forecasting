FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy all backend files (app.py, requirements.txt, model .joblib) into the container
COPY . .

# Install Python dependencies without caching to keep the image lean
RUN pip install --no-cache-dir -r requirements.txt

# Start the Flask app with Gunicorn (4 workers, port 7860)
# 'app:superkart_api' maps to the Flask instance named superkart_api in app.py
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:superkart_api"]
