{% raw %}#!/bin/bash

set -e

OUTPUT=$(pwd)
CERTIFICATE_ATTRIBUTES="/C={{cookiecutter.certificates_country}}/ST={{cookiecutter.certificates_estate}}/L={{cookiecutter.certificates_locality}}/O={{cookiecutter.certificates_organization}}/OU={{cookiecutter.certificates_organizational_unit}}"

generate_certificate() {
	local predicate=$1
	local fqdn=$2
	openssl genrsa -out ${OUTPUT}/certificates/$predicate-key-temp.pem -rand ${OUTPUT}/certificates/.rnd {{ cookiecutter.certificates_bits_length | int }}
	openssl pkcs8 -inform PEM -outform PEM -in ${OUTPUT}/certificates/$predicate-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out ${OUTPUT}/certificates/${predicate}-key.pem
	openssl req -new -key ${OUTPUT}/certificates/${predicate}-key.pem -out ${OUTPUT}/certificates/${predicate}.csr -subj "${CERTIFICATE_ATTRIBUTES}/CN=${fqdn}"
	openssl x509 -req -in ${OUTPUT}/certificates/${predicate}.csr -CA ${OUTPUT}/certificates/root-ca.pem -CAkey ${OUTPUT}/certificates/root-ca-key.pem -CAcreateserial -sha256 -days {{ cookiecutter.certificates_expiration_in_days | int }} -out ${OUTPUT}/certificates/${predicate}.pem

    openssl pkcs12 -export -out ${OUTPUT}/certificates/${predicate}.p12 -inkey ${OUTPUT}/certificates/${predicate}-key.pem -in ${OUTPUT}/certificates/${predicate}.pem -passout pass:""
	rm ${OUTPUT}/certificates/${predicate}-key-temp.pem
	rm ${OUTPUT}/certificates/${predicate}.csr
}

SCRIPT_NAME=$0
SCRIPT_FULL_PATH=$(dirname "$0")

echo "Generate certificates: {{ cookiecutter.generate_deploy_certificates }}"
if [ "true" = "{{ cookiecutter.generate_deploy_certificates | lower }}" ]; then
    echo "##############################################################"
    echo "#                       Generate Root CA                     #"
    echo "##############################################################"
    mkdir -p ${OUTPUT}/certificates
    openssl rand -writerand ${OUTPUT}/certificates/.rnd
    openssl genrsa -out ${OUTPUT}/certificates/root-ca-key.pem -rand ${OUTPUT}/certificates/.rnd {{ cookiecutter.certificates_bits_length | int }}
    openssl req -new -x509 -sha256 -key ${OUTPUT}/certificates/root-ca-key.pem -days {{ cookiecutter.certificates_expiration_in_days | int }} -out ${OUTPUT}/certificates/root-ca.pem -subj "${CERTIFICATE_ATTRIBUTES}/CN={{ cookiecutter.project_slug }}-root"
    openssl pkcs12 -export -nokeys -inkey ${OUTPUT}/certificates/root-ca-key.pem -in ${OUTPUT}/certificates/root-ca.pem -out ${OUTPUT}/certificates/root-ca-no-pkey.p12 -passout pass:""

    echo "##############################################################"
    echo "#                   Generate Strong DH group                 #"
    echo "##############################################################"

    openssl dhparam -out ${OUTPUT}/certificates/dhparam.pem {{ cookiecutter.certificates_bits_length | int }}

    echo "##############################################################"
    echo "#                     Generate Admin cert                    #"
    echo "##############################################################"
    generate_certificate admin admin-prod

    for (( i=1; i<={{ cookiecutter.elastic_nodes }}; i++ ))
    do
        echo "##############################################################"
        echo "#           Generate Elasticsearch Node ${i} cert            #"
        echo "##############################################################"
        generate_certificate node${i} elastic-${i}
    done

    echo "##############################################################"
    echo "#                     Generate Kibana cert                   #"
    echo "##############################################################"
    generate_certificate kibana kibana

    echo "##############################################################"
    echo "#                    Generate Search API Cert                #"
    echo "##############################################################"
    generate_certificate search-api search-api

    echo "##############################################################"
    echo "#                     Generate Search UI Cert                #"
    echo "##############################################################"
    generate_certificate search-ui search-ui

    echo "##############################################################"
    echo "#                     Generate Frontend Cert                 #"
    echo "##############################################################"
    generate_certificate frontend {{ cookiecutter.server_name }}

    rm -rf ${OUTPUT}/certificates/.rnd

    echo "Certificates generated at \"$(readlink -f ${OUTPUT}/certificates)\"."
fi

echo ""
echo "There are other important configurations at :"
echo " - https://opendistro.github.io/for-elasticsearch-docs/docs/install/docker/#important-settings "
echo " - https://www.elastic.co/guide/en/elasticsearch/reference/current/system-config.html "
echo " - https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-prod-prerequisites "
echo ""
echo ""
echo "You can edit/extend the file docker-compose-base.yml and define the volumes configurations differently."
echo ""
echo "To run the app type: 'docker stack deploy -c docker-compose-base.yml {{ cookiecutter.project_slug }}'"

exit 0
{% endraw %}