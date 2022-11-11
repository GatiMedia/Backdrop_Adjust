#encoding=utf-8
# --------------------------------------------------------------
#  BackdropAdjust menu.py
#  Version: 1.6
#  Last Updated: 10/11/2022
# --------------------------------------------------------------

## Imports
import nuke
import Backdrop_Adjust_utils

## Add BackdropAdjust the Toolset
nuke.menu('Nodes').addMenu('Other').addCommand('BackdropAdjust', 'Backdrop_Adjust_utils.create_BD_Adj()', shortcut='Alt+b', icon='Backdrop.png', index=3)

## Add BackdropAdjust(popup) the Toolset
nuke.menu('Nodes').addMenu('Other').addCommand('BackdropAdjust (popup)', 'Backdrop_Adjust_utils.createBDApopup()', shortcut='Alt+Shift+b', icon='Backdrop.png', index=4)
