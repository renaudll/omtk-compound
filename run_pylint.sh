#!/bin/bash

# Find maya
_MAYA_BIN=$(readlink -f `command -v maya`)
_MAYA_DIR=$(dirname "${_MAYA_BIN}")

# Find pylint
_PYLINT_BIN=$(python2 -c "import pylint; print(pylint.__file__)")
_PYLINT_DIR=$(dirname "${_PYLINT_BIN}")
_PYLINT_DIR=$(dirname "${_PYLINT_DIR}")

echo "[setup] Addding to PYTHONPATH: ${_PYLINT_DIR}"
PYTHONPATH="${PYTHONPATH}:${_PYLINT_DIR}"
echo "$PYTHONPATH"

# Export mayapy
echo "[setup] Adding to PATH: ${_MAYA_DIR}"
PATH="${PATH}:${_MAYA_DIR}"

mayapy -m pylint scripts/omtk_compound \
  -f colorized \
  --ignore="vendor,ui" \
  | less --raw
