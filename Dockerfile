FROM python:3.9.2-buster

ARG GITHUB_SHA

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
    && rm -rf /var/lib/apt/lists/*

RUN pip install gunicorn

COPY fonts /usr/local/share/fonts

COPY setup.py .

# Install dev dependencies into main image for now
RUN pip install --no-cache-dir -e '.[dev]'

COPY . .

ENV GITHUB_SHA=$GITHUB_SHA

RUN echo $GITHUB_SHA

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "pdf_service:pdf_service" ]
EXPOSE 8080
