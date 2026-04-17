FROM python:3.11-slim

# Install postgres client libraries
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
RUN pip install flask psycopg2-binary

# Copy your files into the container
COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/

# Flask runs on 5000 by default
EXPOSE 5000

CMD ["python", "app.py", "--host=0.0.0.0"]
