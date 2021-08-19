FROM python:3.9.6-alpine3.14

WORKDIR /usr/src/app

RUN apk add --no-cache \
      gcc \
      musl-dev \
      jpeg-dev \
      zlib-dev \
      libffi-dev \
      cairo-dev \
      pango-dev \
      gdk-pixbuf \
      poppler-dev \
      shared-mime-info \
      ttf-opensans \
      ttf-dejavu \
      ghostscript-fonts

RUN pip install --no-cache-dir gunicorn

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m pdf_service_user && chown pdf_service_user .
USER pdf_service_user

ARG GITHUB_SHA
ENV SENTRY_RELEASE=$GITHUB_SHA

ENV WORKER_COUNT=4

CMD gunicorn -w $WORKER_COUNT -b 0.0.0.0:8080 pdf_service:pdf_service
EXPOSE 8080
