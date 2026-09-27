FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 5000
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python", "-m", "flask", "--app", "app:create_app", "run", "--host=0.0.0.0", "--port=5000"]
