"""
Method for reading and parsing .ma files.
"""

import re
import tempfile
import shutil
from typing import Generator

from ._constants import FILE_METADATA_PREFIX

_REGEX_MA_HEADER = re.compile(r"^//Maya ASCII .* scene")
_REGEX_FILE_INFO = re.compile(r'^fileInfo "(.*)" "(.*)";')


def remove_root_namespace(namespace: str, path: str) -> None:
    """Remove a namespace from a file. Overwrite the file.

    :param namespace: The namespace to remove
    :param path: A path to a file to parse.
    """
    pattern = f'"{namespace.strip(":")}:'
    path_tmp = tempfile.mktemp(suffix=".ma")
    with open(path, "r") as fp_in:
        with open(path_tmp, "w") as fp_out:
            for line in fp_in:
                line = line.replace(pattern, '"')
                fp_out.write(line)

    shutil.move(path_tmp, path)


def write_metadata_to_ma_file(path: str, metadata: dict) -> bool:
    """
    Write metadata to a Maya file.

    :param path:
    :param metadata:
    :return: True if successful, False otherwise
    """
    path_tmp = tempfile.mktemp()
    success = False
    found = False
    with open(path, "r") as fp_read:
        with open(path_tmp, "w") as fp_write:
            line = fp_read.readline()
            if not _REGEX_MA_HEADER.match(line):
                raise Exception(f"Invalid Maya ASCII file {path}")
            fp_write.write(line)

            for line in fp_read:
                regex_result = _REGEX_FILE_INFO.match(line)
                if regex_result:
                    found = True
                    key, val = regex_result.groups()
                    if key.startswith(FILE_METADATA_PREFIX):
                        continue
                elif found:
                    for key, val in metadata.items():
                        val_conformed = val.replace("\n", r"\n")
                        fp_write.write(
                            f'fileInfo "{FILE_METADATA_PREFIX}{key}" "{val_conformed}";\n'
                        )
                    success = True
                    found = False

                fp_write.write(line)

    shutil.move(path_tmp, path)

    return success


def iter_ma_file_metadata(path: str) -> Generator[tuple[str, str], None, None]:
    """
    :param path: An absolute path to a Maya file.
    :return: A key-value pair generator
    """
    with open(path, "r") as fp:
        line = fp.readline()
        if not _REGEX_MA_HEADER.match(line):
            raise Exception(f"Invalid first line for file {path}: {line}")

        found = False
        while fp:
            line = fp.readline()
            regex_result = _REGEX_FILE_INFO.match(line)
            if regex_result:
                found = True
                key, val = regex_result.groups()
                yield key, val
            elif found:
                break


def get_metadata_from_file(path: str) -> dict[str, str | None]:
    """
    Read a file header and return its metadata.

    :param path:
    :return: A metadata dict
    """
    metadata = {}
    for key, val in iter_ma_file_metadata(path):
        if key.startswith(FILE_METADATA_PREFIX):
            key = key[len(FILE_METADATA_PREFIX) :]
            metadata[key] = None if val == "None" else val
    return metadata
