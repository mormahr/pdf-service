FROM python:3.9.1-buster

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

RUN pip install --no-cache-dir -e .

COPY . .

ARG GITHUB_SHA
ENV GITHUB_SHA=$GITHUB_SHA

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app" ]
EXPOSE 8080
