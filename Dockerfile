# author : P B S Alekhya
# date: 2nd june 2025
# last change date : 6th june 2025

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY config.json .
COPY train_model.py .
COPY data ./data


EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
