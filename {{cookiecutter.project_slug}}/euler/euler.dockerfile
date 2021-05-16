ARG DOCKER_TAG=latest

FROM maven as builder

ARG DOCKER_TAG=latest

RUN mkdir /build && cd /build
COPY ./pom.xml /build
COPY ./download-dependencies.sh /build
COPY ./templates /build

COPY ./basic/reference.conf /build
RUN cd /build \
    && jar cvf basic-config.jar reference.conf

# Download dependencies from com.github.euler-io:euler-elasticsearch:$EULER_VERSION
RUN /build/download-dependencies.sh

# Build templates configuration
RUN echo "templates: [" > /build/templates.conf \
    && cat /build/parse-files.conf >> /build/templates.conf \
    && cat /build/add-new-files.conf >> /build/templates.conf \
    && cat /build/delete-files.conf >> /build/templates.conf \
    && cat /build/update-files.conf >> /build/templates.conf \
    && echo "]" >> /build/templates.conf


FROM {{ cookiecutter.docker_image_euler_api }}

