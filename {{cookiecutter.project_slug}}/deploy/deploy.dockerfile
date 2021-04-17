FROM python:3-slim

COPY ./extensions/* /extensions/
ENV PYTHONPATH "${PYTHONPATH}:/extensions"
#ENV OUTPUT="."
#ENV TEMPLATE="/deploy"

RUN mkdir -p /cookiecutter/replay-dir \
    && chmod 777 -R /cookiecutter \
    && echo 'replay_dir: "/cookiecutter/replay-dir"' > /cookiecutter/config.yaml
ENV COOKIECUTTER_CONFIG "/cookiecutter/config.yaml"

COPY requirements.txt .
RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt 

CMD ["/bin/bash", "-c"]