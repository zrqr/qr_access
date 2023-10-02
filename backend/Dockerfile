FROM python:3.11-slim

COPY . .

RUN apt-get update
RUN apt-get install ffmpeg python3-libgpiod htop -y
RUN pip install -r requirements.txt

WORKDIR /django_project
CMD python manage.py runserver 192.168.0.17:8000
