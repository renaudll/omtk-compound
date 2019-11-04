import mock
import pytest
from omtk_compound import CompoundDefinition, Registry
from omtk_compound.widgets.models.model_registry import CompoundRegistryModel
from omtk_compound.vendor.Qt import QtCore


@pytest.fixture
def registry():
    inst = Registry()
    inst.register(CompoundDefinition(name="component1", version="0.0.1"))
    inst.register(CompoundDefinition(name="component1", version="0.0.2"))
    inst.register(CompoundDefinition(name="component2", version="0.1.0"))
    return inst


@pytest.fixture
def model(registry):
    return CompoundRegistryModel(registry)


def test_headerData(model):  # type: (CompoundRegistryModel) -> None
    """ Validate our implementation of :
    - `QAbstractItemModel.headerData`
    - `QAbstractItemModel.rowCount`
    """
    expected = ["name", "version", "author"]
    actual = [
        model.headerData(row, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole)
        for row in range(model.rowCount(None))
    ]
    assert actual == expected


def test_data(model):  # type: (CompoundRegistryModel) -> None
    """
    Validate our implementation of:
    - `QAbstractItemModel.data`
    - `QAbstractItemModel.rowCount`
    - `QAbstractItemModel.columnCount`
    """
    expected = [
        ["component1", "0.0.1", ""],
        ["component1", "0.0.2", ""],
        ["component2", "0.1.0", ""],
    ]
    actual = [
        [
            model.data(model.createIndex(row, col), QtCore.Qt.DisplayRole)
            for col in range(model.columnCount(None))
        ]
        for row in range(model.rowCount(None))
    ]
    assert actual == expected
