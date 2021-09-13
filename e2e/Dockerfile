FROM alpine:3.14

WORKDIR /root
ENV PDF_SERVICE_URL=http://pdf:8080
VOLUME /root/diffs

RUN apk add --no-cache \
      tini \
      bash \
      curl \
      imagemagick

ADD . .

CMD tini ./scripts/run.sh
