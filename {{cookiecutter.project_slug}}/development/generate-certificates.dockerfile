FROM alpine:latest

ENV OUTPUT=/output/certificates

RUN apk add --update openssl bash && \
    rm -rf /var/cache/apk/*

COPY generate_certificates.sh /

ENTRYPOINT ["bash", "/generate_certificates.sh"]