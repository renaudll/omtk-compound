import pytest

from omtk_compound.core._definition import CompoundDefinition


@pytest.fixture
def compdef():
    return CompoundDefinition(name="test_name")


def test_get_uid():
    """Validate creating two compounds will have difference uids."""
    c1 = CompoundDefinition(name="compound_a")
    c2 = CompoundDefinition(name="compound_b")
    assert c1.uid != c2.uid


def test_basic(compdef):
    """Validate CompoundDefinition act like a dict."""
    c = compdef

    # __getitem__
    with pytest.raises(KeyError):
        _ = c["foo"]

    # __setitem__
    c["foo"] = "bar"

    # __getitem__
    assert c["foo"] == "bar"

    # __delitem__
    del c["foo"]

    # __getitem__
    assert "foo" not in c


def test_properties():
    """Test the helper properties."""
    inst = CompoundDefinition(
        uid="test_uid", name="test_name", author="test_author", version="test_version", path="some_path"
    )
    assert inst.uid == "test_uid"
    assert inst.name == "test_name"
    assert inst.author == "test_author"
    assert inst.version == "test_version"
    assert inst.path == "some_path"


def test_missing_field():
    """Validate we raise an error if we fail to provide all mandatory fields."""
    with pytest.raises(ValueError) as error:
        CompoundDefinition()

    assert str(error.value) == "Missing mandatory fields: 'name'"


def test_from_file(cmds, tmp_path, compdef):
    """Validate we can write a compound definition to an existing file. WIP"""
    # Write compound definition (without it's compound body) to a maya ASCII file
    path = str(tmp_path / "def.ma")
    cmds.file(rename=path)
    cmds.file(save=True, type="mayaAscii")
    compdef.write_metadata_to_file(path)

    # Validate we can read the metadata back
    expected = compdef
    expected["path"] = path
    actual = CompoundDefinition.from_file(path)
    assert actual == expected
