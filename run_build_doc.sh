#!/bin/bash

# Find maya
_MAYA_BIN=$(readlink -f `command -v maya`)
_MAYA_DIR=$(dirname "${_MAYA_BIN}")

# Find dir
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Export omtk
PYTHON_DIR="${DIR}/scripts"
echo "[setup] Adding to PYTHONPATH: ${PYTHON_DIR}"
PYTHONPATH="${PYTHON_DIR}:{$PYTHONPATH}"

# Export mayapy
echo "[setup] Adding to PATH: ${_MAYA_DIR}"
PATH="${PATH}:${_MAYA_DIR}"

# Export
MAYA_PYTHONPATH="${_MAYA_DIR}/../lib/python2.7/site-packages"
echo "[setup] Adding to PYTHONPATH: ${MAYA_PYTHONPATH}"
PYTHONPATH="${PYTHONPATH}:${MAYA_PYTHONPATH}"

sphinx-apidoc -f -o ./docs/source scripts/omtk_compound scripts/omtk_compound/vendor
cd docs && make html
