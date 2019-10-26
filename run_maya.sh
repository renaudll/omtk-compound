#!/bin/bash
# Launch maya with the module available

# Expose omtk
# TODO: Expose via maya module
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PYTHONDIR="${DIR}/scripts"
MODULE_DIR="${DIR}"
echo "[setup] Adding to PYTHONPATH: ${PYTHONDIR}"
export MAYA_MODULE_PATH="${MODULE_DIR}:${MAYA_MODULE_PATH}"

# Expose mayapy
_MAYA_BIN=$(readlink -f `command -v maya`)
_MAYA_DIR=$(dirname "${_MAYA_BIN}")
echo "[setup] Adding to PATH: ${_MAYA_DIR}"
PATH="${PATH}:${_MAYA_DIR}"

export OMTK_COMPONENT_DEFAULT_AUTHOR="Renaud Lessard Larouche"

# Run unit tests
maya
