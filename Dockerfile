FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY weather_server.py server.py ./

EXPOSE 8000

CMD ["python", "server.py"]
