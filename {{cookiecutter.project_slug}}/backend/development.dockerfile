FROM python:3.8-slim-buster

COPY ./app/requirements.txt .
RUN pip3 install --upgrade pip \
   && pip3 install -r requirements.txt \
   && pip3 install uvicorn lorem names