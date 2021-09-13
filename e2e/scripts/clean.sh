#!/bin/bash

set -e

cd "$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd -P )" || exit

rm -f ../data/**/diff.png
rm -f ../data/**/generated.*
