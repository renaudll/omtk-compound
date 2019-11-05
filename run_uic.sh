#!/bin/bash
# Compile ui files to py

_UI_DIR=$(pwd)/scripts/omtk_compound/widgets/ui
echo "UI Directory is: ${_UI_DIR}"

source bootstrap.sh

FILES="${_UI_DIR}/*.ui"
for FILE_UI in $FILES
do
  _BASENAME=$(basename "$FILE_UI" ".ui")
  _DIRNAME=$(dirname "$FILE_UI")
  FILE_PY="${_DIRNAME}/${_BASENAME}.py"
  FILE_PY_BACKUP="${_DIRNAME}/${_BASENAME}_backup.py"  # Created by Qt.py

  if [[ $FILE_UI -nt $FILE_PY ]]; then  # If more recent of target don't exist
    echo "Processing $FILE_UI"

    # Compile ui to py
    mayapy -c "import pyside2uic; print pyside2uic; pyside2uic.compileUi('${FILE_UI}', open('${FILE_PY}', 'w'))"

    # Replace PySide2 imports by Qt imports
    mayapy -m Qt --convert "${FILE_PY}"

    # Redirect Qt import to our vendored namespace
    sed -i "s/from Qt/from omtk_compound.vendor.Qt/g" "${FILE_PY}"

    # Remove _backup file created by Qt.py
    rm -f "$FILE_PY_BACKUP"
  fi
done
