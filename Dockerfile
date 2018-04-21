#FROM ubuntu:14.04
FROM python:3.6.4
MAINTAINER winhtaikaung(winhtaikaung28@hotmail.com)

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY . /usr/src/app
ENV DB_HOST=192.168.0.110
COPY run.sh /usr/src/app/
EXPOSE 5000


CMD sh  /usr/src/app/run.sh
