FROM python:3.9.3-buster

WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get install -y \
        build-essential \
        libcairo2 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libgdk-pixbuf2.0-0 \
        libffi-dev \
        shared-mime-info \
        poppler-utils \
        fonts-open-sans \
        fonts-dejavu \
        gsfonts \
    && rm -rf /var/lib/apt/lists/*

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
