FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

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
         libreoffice

COPY ./app /app
RUN pip install -r /app/requirements.txt \
    && pip install lorem names

# Cleaning image.
RUN apt-get clean  \
	&& rm -rf /var/lib/apt/lists/* \
	&& apt-get autoremove -y