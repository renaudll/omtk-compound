#!/bin/bash
# Linux bash script to simplify testing omtk with pytest
source bootstrap.sh

# Run unit tests
mayapy -m "py.test" "$@" --cov=omtk_compound --cov-branch --cov-report term-missing --cov-report html
