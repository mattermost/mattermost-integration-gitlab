FROM python:2.7.11

MAINTAINER "Matt Martz <matt.martz@gmail.com>"

COPY . /src

RUN cd /src; pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT cd /src; python server.py
