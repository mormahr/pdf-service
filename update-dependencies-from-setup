#!/bin/sh

set -e
set -x

pip3 install -e .
pip3 freeze > requirements.txt

pip3 install -e ".[dev]"
pip3 freeze > requirements-dev.txt

grep -Fvx -f requirements.txt requirements-dev.txt >extra.txt &&
mv extra.txt requirements-dev.txt
