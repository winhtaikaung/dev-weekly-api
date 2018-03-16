#FROM ubuntu:14.04
FROM python:3.6.4
MAINTAINER winhtaikaung(winhtaikaung28@hotmail.com)

RUN apt-get update
RUN apt-get install varnish -y
COPY varnish /etc/default/ -y
COPY default.vcl /etc/default/ -y

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY . /usr/src/app
COPY run.sh /usr/src/app/
EXPOSE 5000

CMD service varnish restart
CMD varnishstat

CMD sh python /usr/src/app/app.py