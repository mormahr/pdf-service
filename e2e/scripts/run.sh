#!/bin/bash

if [ "$PDF_SERVICE_URL" = "" ]; then
  echo "\$PDF_SERVICE_URL has to be set."
fi

# Wait for pdf service to become available. (1s retry, 30s timeout)
timeout 30 bash -c 'while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' $PDF_SERVICE_URL/health)" != "200" ]]; do sleep 1; done' || false

cd "$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd -P )" || exit

for f in ../data/*
do
  # Guard against empty directory
  [ -e "$f" ] || continue
  echo "Running $(basename "$f")"

  # Propagate errors because -e isn't set
  "$f/run.sh" || exit 1
done
