FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY webhook-server.py ./

EXPOSE 5001
CMD ["python", "webhook-server.py"]
