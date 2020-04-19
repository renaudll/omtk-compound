"""
This file is executed automatically by maya at startup.
"""
# pylint: disable=invalid-name
from omtk_compound import bootstrap
from maya import cmds

cmds.evalDeferred(bootstrap.bootstrap)
