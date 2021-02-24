FROM python:3.9.2-buster

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
        fonts-open-sans \
        fonts-dejavu \
        gsfonts \
    && rm -rf /var/lib/apt/lists/*

RUN pip install gunicorn

COPY setup.py .

RUN pip install --no-cache-dir -e .

COPY . .

ARG GITHUB_SHA
ENV GITHUB_SHA=$GITHUB_SHA
RUN echo $GITHUB_SHA

ENV WORKER_COUNT=4

CMD gunicorn -w $WORKER_COUNT -b 0.0.0.0:8080 pdf_service:pdf_service
EXPOSE 8080
