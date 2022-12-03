#encoding=utf-8
# --------------------------------------------------------------
#  BackdropAdjust menu.py
#  Version: 1.8
#  Last Updated: 21/11/2022
# --------------------------------------------------------------

## Imports
import nuke
import os
import Backdrop_Adjust_utils
import Backdrop_Adjust_search

## Current file path for the icons
BDA_path = os.path.dirname(__file__)

## Creating BDA menu
BDA_menu = nuke.menu('Nodes').addMenu('Other').addMenu('BackdropAdjust_tools', icon = os.path.join(BDA_path, "icon/bda_icon_2.png"), index=3)

## Add BackdropAdjust(node) the Toolset
BDA_menu.addCommand('BackdropAdjust(node)', 'Backdrop_Adjust_utils.create_BD_Adj()', shortcut='Alt+b', icon = os.path.join(BDA_path, "icon/bda_icon.png"), index=0)

## Add BackdropAdjust(popup) the Toolset
BDA_menu.addCommand('BackdropAdjust(popup)', 'Backdrop_Adjust_utils.createBDApopup()', shortcut='Alt+Shift+b', icon = os.path.join(BDA_path, "icon/bda_icon.png"), index=1)

## Add BackdropAdjust(search) the Toolset
BDA_menu.addCommand('BackdropAdjust(search)', 'Backdrop_Adjust_search.createBDASearchPopup()', shortcut='Ctrl+Shift+b', icon = os.path.join(BDA_path, "icon/bda_icon.png"), index=2)
