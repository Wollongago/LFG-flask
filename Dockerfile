FROM python:3.9.13-slim-bullseye

LABEL maintainer="lonnstyle"

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN groupadd -r -g 1000 pygroup && useradd -m -r -g pygroup -u 1000 pyuser
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
COPY requirements.txt requirements.txt
RUN apt-get install -y wget \
    python3-pip \
    locales && \
    pip3 install --upgrade pip setuptools && \
    pip3 install -r requirements.txt

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz && \
    rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Setup UTF-8
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8     

COPY docker /build

RUN mv /build/celery.sh /usr/local/bin
RUN mv /build/http.sh /usr/local/bin

# Remove build files
RUN rm -rf /build


# Copy Application sources
COPY src/*.py /application/
COPY src/Extensions /application/Extensions
COPY src/Application /application/Application
COPY src/Celery /application/Celery

# Set exit signal
STOPSIGNAL SIGINT
