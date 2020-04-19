"""Test for omtk_compound.models.model_compound"""
# pylint: disable=redefined-outer-name
import mock
import pytest

from omtk_compound import Compound
from omtk_compound.models import ModelAttributes
from omtk_compound.vendor.Qt import QtCore


@pytest.fixture
def compound(cmds):
    """Fixture for a preconfigured compound"""
    cmds.namespace(addNamespace="testCompound")

    cmds.createNode("network", name="testCompound:inputs")
    cmds.createNode("transform", name="testCompound:node")
    cmds.createNode("network", name="testCompound:outputs")

    cmds.addAttr("testCompound:inputs", longName="testAttr2")
    cmds.addAttr("testCompound:inputs", longName="testAttr1")

    return Compound("testCompound")


@pytest.fixture
def model(compound):
    """Fixture for a preconfigured model"""
    return ModelAttributes(sorted(compound.inputs))


def test_headerData(model):  # pylint: disable=invalid-name
    """ Validate our implementation of `QAbstractItemModel.headerData`. """
    expected = ["name", "type", "multi"]
    actual = [
        model.headerData(row, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole)
        for row in range(3)
    ]
    assert actual == expected


def test_data(model):
    """
    Validate our implementation of:
    - `QAbstractItemModel.data`
    - `QAbstractItemModel.rowCount`
    - `QAbstractItemModel.columnCount`
    """
    expected = [
        ["testAttr1", "double", "False"],
        ["testAttr2", "double", "False"],
    ]
    actual = [
        [
            model.data(model.index(row, col), QtCore.Qt.DisplayRole)
            for col in range(model.columnCount())
        ]
        for row in range(model.rowCount())
    ]
    assert actual == expected


def test_setData(cmds, model):  # pylint: disable=invalid-name
    """Validate our implementation `QAbstractItemMode.setData`. """
    model.setData(model.index(0, 0), "zTestAttr1", QtCore.Qt.EditRole)

    # Validate the attribute was moved in maya
    assert not cmds.objExists("testCompound:inputs.testAttr1")
    assert cmds.objExists("testCompound:inputs.zTestAttr1")

    # Validate the UI display reordered values
    assert model.data(model.index(0, 0), QtCore.Qt.DisplayRole) == "zTestAttr1"
    assert model.data(model.index(1, 0), QtCore.Qt.DisplayRole) == "testAttr2"


def test_setData_name_clash(cmds, model):  # pylint: disable=invalid-name
    """Validate we cannot rename an attribute to a another existing one. """
    with mock.patch.object(cmds, "warning", side_effect=cmds.warning) as mocked_warning:
        # Note: "testAttr2" already exist
        model.setData(model.index(0, 0), "testAttr2", QtCore.Qt.EditRole)

    # Validate the attribute was NOT moved in maya
    assert cmds.objExists("testCompound:inputs.testAttr1")
    assert not cmds.objExists("testCompound:inputs.zTestAttr1")

    # Validate the UI still display the same values
    assert model.data(model.index(0, 0), QtCore.Qt.DisplayRole) == "testAttr1"
    assert model.data(model.index(1, 0), QtCore.Qt.DisplayRole) == "testAttr2"

    # Validate the user saw a warning
    assert mocked_warning.mock_calls == [
        mock.call("Attribute 'testCompound:inputs.testAttr2' already exist.")
    ]
