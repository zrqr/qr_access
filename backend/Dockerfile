FROM python:3.11-slim

COPY . .

RUN apt-get update
RUN apt-get install ffmpeg python3-libgpiod htop -y
RUN pip install -r requirements.txt

CMD bash
