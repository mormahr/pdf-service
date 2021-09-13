#!/bin/sh

set -e

convert -density 200 -depth 8 -quality 100 generated.pdf -background white -flatten -strip PNG24:$1
