"""Test various compound update scenarios"""
import pytest

from omtk_compound.core import Compound


@pytest.fixture
def compound(scene):
    return Compound("test")


@pytest.fixture
def compound_v1(cmds, tmp_path, compound):
    cmds.file(new=True, force=True)
    cmds.createNode("transform", name="foo")
    p = tmp_path / "compound-v1.ma"
    compound.export(p)


@pytest.fixture
def compound_v2(cmds, tmp_path, compound):
    cmds.file(new=True, force=True)
    cmds.createNode("transform", name="bar")
    p = tmp_path / "compound-v2.ma"
    compound.export(p)


@pytest.fixture
def compound_versions(compound_v1, compound_v2):
    return None
