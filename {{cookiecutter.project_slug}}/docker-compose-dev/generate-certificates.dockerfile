FROM alpine:latest

ENV OUTPUT=/certicates

RUN apk add --update openssl bash && \
    rm -rf /var/cache/apk/*

COPY generate_certificates.sh /

VOLUME certificates
ENTRYPOINT ["bash", "/generate_certificates.sh"]