#!/bin/bash

set -e

if [ ! -f reference.png ]; then
  # Reference file doesn't exist yet -> create
  echo "Generating for $(basename "$PWD")"
  ../../scripts/convert.sh reference.png
else
  ../../scripts/convert.sh generated.png

  # Remove old diffs
  mkdir -p ../../diffs/
  rm -f "../../diffs/$(basename "$PWD").*"

  # Create diff image
  # Ignore comparison errors here because we do a byte comparison later
  compare reference.png generated.png -compose Src "../../diffs/$(basename "$PWD").png" || true

  # Generate animated GIF to illustrate differences
  convert -delay 50 reference.png generated.png -loop 0 "../../diffs/$(basename "$PWD").gif"

  # Byte comparison of reference and current image
  if ! cmp reference.png generated.png > /dev/null 2>&1
  then
    echo "Reference and generated image differ for $(basename "$PWD")"
    exit 1
  fi
fi
