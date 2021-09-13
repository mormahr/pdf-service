#!/bin/bash

set -e

cd "$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd -P )" || exit

./clean.sh
rm -f ../data/**/reference.png
./run.sh
