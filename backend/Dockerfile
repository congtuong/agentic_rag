
FROM python:3.9-slim

WORKDIR /app

RUN apt update && apt upgrade -y && apt install -y git

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./app /app/app

COPY ./.env /app/.env

CMD ["python", "app/main.py"]