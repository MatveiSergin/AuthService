FROM python:3.12.3-bookworm

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/home/developer/AuthService/backend/app

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

COPY . /usr/src/app/