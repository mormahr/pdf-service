FROM python:3.9.7-alpine3.14

WORKDIR /usr/src/app

RUN apk add --no-cache \
      gcc \
      musl-dev \
      python3-dev \
      jpeg-dev \
      zlib-dev \
      libffi-dev \
      openssl-dev \
      cargo \
      cairo-dev \
      pango-dev \
      gdk-pixbuf \
      shared-mime-info \
      poppler-utils \
      poppler-dev \
      # fonts
      ttf-opensans \
      ttf-dejavu \
      ghostscript-fonts \
      # curl is needed for the status check
      curl

RUN pip install --no-cache-dir gunicorn

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN addgroup -S pdf_service_group && \
    adduser --uid 1001 -S pdf_service_user -G pdf_service_group && \
    chown pdf_service_user .
USER pdf_service_user

ARG GITHUB_SHA
ENV SENTRY_RELEASE=$GITHUB_SHA

ENV WORKER_COUNT=4

HEALTHCHECK --interval=2s --timeout=2s --retries=5 --start-period=2s CMD curl --fail http://localhost:8080/health || exit 1

CMD exec gunicorn -w $WORKER_COUNT -t 0 -b 0.0.0.0:8080 pdf_service:pdf_service
EXPOSE 8080
