FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

# Run Streamlit on port 8501, accessible from any network interface
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]
