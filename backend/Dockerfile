FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Moscow

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir

EXPOSE 8000

WORKDIR /backend
COPY . /backend