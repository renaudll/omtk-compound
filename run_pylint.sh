#!/bin/bash

source bootstrap.sh

# Find pylint
_PYLINT_BIN=$(python2 -c "import pylint; print(pylint.__file__)")
_PYLINT_DIR=$(dirname "${_PYLINT_BIN}")
_PYLINT_DIR=$(dirname "${_PYLINT_DIR}")

mayapy -m pylint scripts/omtk_compound \
  -f colorized \
  --ignore="vendor,ui" \
  | less --raw
