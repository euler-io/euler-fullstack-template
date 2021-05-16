FROM python:3.8-slim-buster

RUN apt-get update \
   && mkdir -p /usr/share/man/man1 \
   && apt-get install -y --no-install-recommends \
         openjdk-11-jre-headless \
         zlib1g-dev \
         libjpeg-dev \
         python3-pythonmagick \
         inkscape \
         xvfb \
         poppler-utils \
         libfile-mimeinfo-perl \
         qpdf \
         libimage-exiftool-perl \
         ufraw-batch \
         ffmpeg \
         libreoffice \
         libmagic1

COPY ./app/requirements.txt .
RUN pip3 install --upgrade pip \
   && pip3 install -r requirements.txt \
   && pip3 install uvicorn lorem names

# Cleaning image.
RUN apt-get clean  \
	&& rm -rf /var/lib/apt/lists/* \
	&& apt-get autoremove -y