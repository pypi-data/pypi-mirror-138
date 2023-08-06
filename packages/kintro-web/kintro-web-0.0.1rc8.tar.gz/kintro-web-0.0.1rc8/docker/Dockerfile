ARG PYTHON_VERSION
ARG PYTHON_BASE
ARG PYTHON_IMAGE=python:${PYTHON_VERSION}-${PYTHON_BASE}
FROM ${PYTHON_IMAGE} as kintro-web-base

ENV PYTHON_VERSION=${PYTHON_VERSION}

# SLOWISH
RUN apk add gcc \
            python3-dev \
            musl-dev \
            linux-headers \
            g++ \
	    git \
	    jq \
	    bash

VOLUME ["/data"]
EXPOSE 8080



FROM kintro-web-base as kintro-web-repo

ARG KINTRO_WEB_REPO=https://github.com/neckbeard-io/kintro-web.git
ARG KINTRO_WEB_BRANCH=main

RUN git clone ${KINTRO_WEB_REPO} kintro-web \
      && cd kintro-web \
      && git checkout ${KINTRO_WEB_BRANCH} \
      && pip install -e . \
      && pip install uwsgi

WORKDIR kintro-web

ENTRYPOINT ["uwsgi", "docker/uwsgi_repo_conf.ini"]



FROM kintro-web-base as kintro-web-pkg

ARG KINTRO_VERSION=0.0.1rc4
ARG KINTRO_WEB_VERSION=0.0.1rc4

COPY uwsgi_conf.ini /uwsgi_conf.ini

RUN pip install kintro==${KINTRO_VERSION} kintro-web==${KINTRO_WEB_VERSION} \
      && pip install uwsgi

ENTRYPOINT ["uwsgi", "/uwsgi_conf.ini"]
