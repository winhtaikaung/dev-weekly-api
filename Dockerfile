FROM python:3.6.4
MAINTAINER winhtaikaung(winhtaikaung28@hotmail.com)

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY . /usr/src/app
COPY run.sh /usr/src/app/
ENV DB_HOST=db_dev_weekly
EXPOSE 5000


CMD sh  /usr/src/app/run.sh
