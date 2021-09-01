FROM python:3.9.7-alpine3.14 AS builder

WORKDIR /usr/src/app

RUN apk add --no-cache \
      gcc \
      g++ \
      musl-dev \
      python3-dev \
      jpeg-dev \
      openjpeg-dev \
      zlib-dev \
      libffi-dev \
      openssl-dev \
      pango-dev \
      gdk-pixbuf \
      shared-mime-info \
      # fonts
      ttf-opensans \
      ttf-dejavu \
      ghostscript-fonts \
      # Used as the entrypoint
      tini \
      # curl is needed for the status check
      curl

RUN pip install --no-cache-dir gunicorn

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM builder AS testing
# Testing stage only for local testing, edit ci.yml test job accordingly.
RUN apk add --no-cache \
      cargo \
      poppler-utils \
      poppler-dev

ADD requirements-dev.txt .

RUN pip install --no-cache-dir -r requirements-dev.txt

RUN addgroup -S pdf_service_group && \
    adduser --uid 1001 -S pdf_service_user -G pdf_service_group && \
    chown pdf_service_user .
USER pdf_service_user

COPY . .

ARG GITHUB_SHA
ENV SENTRY_RELEASE=$GITHUB_SHA

FROM builder AS production
# Named stage so it can be optimized in the future. (Stage name is referenced by CI build script.)


RUN addgroup -S pdf_service_group && \
    adduser --uid 1001 -S pdf_service_user -G pdf_service_group && \
    chown pdf_service_user .
USER pdf_service_user

COPY . .

ARG GITHUB_SHA
ENV SENTRY_RELEASE=$GITHUB_SHA

ENV WORKER_COUNT=4

HEALTHCHECK --interval=2s --timeout=2s --retries=5 --start-period=2s CMD curl --fail http://localhost:8080/health || exit 1

CMD tini gunicorn -w $WORKER_COUNT -t 0 -b 0.0.0.0:8080 pdf_service:pdf_service
EXPOSE 8080
