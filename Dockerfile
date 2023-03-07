# syntax=docker/dockerfile:1
FROM python3.10:slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app/
COPY requirements.txt /app/
RUN pip install -r requirements.txt
