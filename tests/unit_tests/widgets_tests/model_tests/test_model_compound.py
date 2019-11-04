import mock
import pytest
from omtk_compound import Compound
from omtk_compound.widgets.models.model_compound import ModelCompoundInputs, ModelCompoundOutputs
from omtk_compound.vendor.Qt import QtCore


@pytest.fixture
def compound(cmds):
    cmds.namespace(addNamespace="testCompound")

    cmds.createNode("network", name="testCompound:inputs")
    cmds.createNode("transform", name="testCompound:node")
    cmds.createNode("network", name="testCompound:outputs")

    cmds.addAttr("testCompound:inputs", longName="testAttr2")
    cmds.addAttr("testCompound:inputs", longName="testAttr1")

    return Compound("testCompound")


@pytest.fixture
def model(compound):
    return ModelCompoundInputs(compound)


def test_headerData(model):  # type: (ModelCompoundInputs) -> None
    """ Validate our implementation of `QAbstractItemModel.headerData`. """
    expected = ["name", "type", "multi"]
    actual = [
        model.headerData(row, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole) for row in range(3)
    ]
    assert actual == expected


def test_data(model):  # type: (ModelCompoundInputs) -> None
    """
    Validate our implementation of:
    - `QAbstractItemModel.data`
    - `QAbstractItemModel.rowCount`
    - `QAbstractItemModel.columnCount`
    """
    expected = [
        ["testAttr1", "not implemented", "not implemented"],
        ["testAttr2", "not implemented", "not implemented"],
    ]
    actual = [
        [
            model.data(model.createIndex(row, col), QtCore.Qt.DisplayRole)
            for col in range(model.columnCount(None))
        ]
        for row in range(model.rowCount(None))
    ]
    assert actual == expected


@pytest.mark.parametrize("role", (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole))
def test_setData(cmds, model, role):  # type: (ModuleType, ModelCompoundInputs, int) -> None
    """Validate our implementation `QAbstractItemMode.setData`. """
    model.setData(model.createIndex(0, 0), "zTestAttr1", role)

    # Validate the attribute was moved in maya
    assert not cmds.objExists("testCompound:inputs.testAttr1")
    assert cmds.objExists("testCompound:inputs.zTestAttr1")

    # Validate the UI display reordered values
    assert model.data(model.createIndex(0, 0), QtCore.Qt.DisplayRole) == "testAttr2"
    assert model.data(model.createIndex(1, 0), QtCore.Qt.DisplayRole) == "zTestAttr1"


def test_setData_name_clash(cmds, model):  # type: (ModuleType, ModelCompoundInputs) -> None
    """Validate we cannot rename an attribute to a another existing one. """
    with mock.patch.object(cmds, "warning", side_effect=cmds.warning) as mocked_warning:
        # Note: "testAttr2" already exist
        model.setData(model.createIndex(0, 0), "testAttr2", QtCore.Qt.EditRole)

    # Validate the attribute was NOT moved in maya
    assert cmds.objExists("testCompound:inputs.testAttr1")
    assert not cmds.objExists("testCompound:inputs.zTestAttr1")

    # Validate the UI still display the same values
    assert model.data(model.createIndex(0, 0), QtCore.Qt.DisplayRole) == "testAttr1"
    assert model.data(model.createIndex(1, 0), QtCore.Qt.DisplayRole) == "testAttr2"

    # Validate the user saw a warning
    assert mocked_warning.mock_calls == [
        mock.call("Attribute 'testCompound:inputs.testAttr2' already exist.")
    ]
