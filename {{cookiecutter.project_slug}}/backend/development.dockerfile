FROM python:latest

COPY requirements.txt .
RUN pip3 install --upgrade pip \
   && pip3 install -r requirements.txt \
   && pip3 install uvicorn lorem names