#!/bin/bash

set -e

if [ "$PDF_SERVICE_URL" = "" ]; then
  echo "\$PDF_SERVICE_URL has to be set."
fi

cd "$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )"

curl \
  --fail \
  --silent \
  -F index.html=@index.html \
  "$PDF_SERVICE_URL/generate" \
  > generated.pdf

../../scripts/create_reference_or_diff.sh
