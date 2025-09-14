FROM python:3.11.13

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY movie_client.py .
ENTRYPOINT  ["python", "movie_client.py"]