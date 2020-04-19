"""
Common pytest fixtures
"""
# pylint: disable=redefined-outer-name
import pytest


@pytest.fixture(scope="session")
def maya_standalone():
    """Fixture that initialize maya standalone"""
    from maya import standalone

    standalone.initialize()

    yield

    standalone.uninitialize()


@pytest.fixture(autouse=True)
def maya_scene(maya_standalone):  # pylint: disable=unused-argument
    """Fixture that create a new maya scene"""
    from maya import cmds

    cmds.file(new=True, force=True)


@pytest.fixture
def cmds(maya_standalone):  # pylint: disable=unused-argument
    """Fixture for the maya.cmds module"""
    from maya import cmds

    return cmds
