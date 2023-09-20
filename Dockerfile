FROM python:latest
WORKDIR /data_link_api
COPY /requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r /requirements.txt
COPY . /data_link_api

