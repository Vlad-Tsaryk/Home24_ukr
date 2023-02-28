# syntax=docker/dockerfile:1
FROM python:3.10

WORKDIR /home/app/home24

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install psycopg2 dependencies
RUN apt-get update && apt-get -y install gcc python3-dev musl-dev

RUN pip install --upgrade pip
# copy project
COPY . /home/app/home24
RUN apt update
RUN apt-get -y install wkhtmltopdf
RUN pip install -r requirements.txt
