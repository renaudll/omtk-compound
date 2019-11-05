#!/bin/bash
# Linux bash script to simplify testing omtk with pytest

# Initialize environment
source bootstrap.sh

# Run unit tests
mayapy "$@"
