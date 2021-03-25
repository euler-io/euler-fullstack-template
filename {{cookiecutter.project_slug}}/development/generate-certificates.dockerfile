FROM alpine:latest

ENV OUTPUT=/output/certificates

RUN apk add --update openssl bash && \
    rm -rf /var/cache/apk/*

COPY generate_certificates.sh /

CMD sed 's/\r$//' '/generate_certificates.sh' | bash
