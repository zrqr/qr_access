FROM python:3.11-slim

COPY . .

RUN apt-get update
RUN apt-get install ffmpeg -y
RUN apt-get install python3-libgpiod -y
RUN pip install -r requirements.txt


