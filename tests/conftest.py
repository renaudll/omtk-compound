import pytest


@pytest.fixture(scope='session')
def maya_standalone():
    from maya import standalone
    standalone.initialize()


@pytest.fixture(autouse=True)
def maya_scene(maya_standalone):
    from maya import cmds
    cmds.file(new=True, force=True)

#
# @pytest.fixture
# def session():
#     return MockedSession()
#
#
# @pytest.fixture
# def cmds_mock(session):
#     return MockedCmdsSession(session)
#
@pytest.fixture
def cmds_maya(maya_standalone):
    from maya import cmds
    return cmds


@pytest.fixture
def cmds(cmds_maya):
    """Use maya_mock by default"""
    return cmds_maya
