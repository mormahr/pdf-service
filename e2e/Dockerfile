FROM alpine:3.14

WORKDIR /root
ENV PDF_SERVICE_URL=http://pdf:8080
VOLUME /root/diffs

RUN apk add --no-cache \
      bash \
      curl \
      imagemagick

ADD . .

CMD [ "/bin/bash", "./scripts/run.sh" ]
