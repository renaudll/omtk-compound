#!/bin/bash

# Initialize environment
source bootstrap.sh

# Generate documentation with sphinx
sphinx-apidoc -f -o ./docs/source scripts/omtk_compound scripts/omtk_compound/vendor

# Generate html documentation with make
cd docs && make html
