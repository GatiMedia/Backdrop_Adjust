#encoding=utf-8
# --------------------------------------------------------------
#  BackdropAdjust menu.py
#  Version: 2.0
#  Last Updated: 27/08/2024
#  Last updated by: Attila Gasparetz
# --------------------------------------------------------------

## Imports
import nuke
import os
import Backdrop_Adjust_utils
import Backdrop_Adjust_search
import Backdrop_Adjust_advanced

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

BDA_menu.addSeparator()

def all_to_fill():
    for bd in nuke.allNodes('BackdropNode'):
        try:
            bd['appearance'].setValue('Fill')
            bd['appearance_custom'].setValue('Fill')
        except:
            pass

def all_to_border():
    for bd in nuke.allNodes('BackdropNode'):
        try:
            bd['appearance'].setValue('Border')
            bd['appearance_custom'].setValue('Border')
        except:
            pass

def sel_to_fill():
    for bd in nuke.selectedNodes('BackdropNode'):
        try:
            bd['appearance'].setValue('Fill')
            bd['appearance_custom'].setValue('Fill')
        except:
            pass

def sel_to_border():
    for bd in nuke.selectedNodes('BackdropNode'):
        try:
            bd['appearance'].setValue('Border')
            bd['appearance_custom'].setValue('Border')
        except:
            pass

BDA_appearance_menu = BDA_menu.addMenu('Appearance', icon = os.path.join(BDA_path, "icon/bda_icon_3.png"), index=3)

## Add all_to_fill() to the Toolset
BDA_appearance_menu.addCommand('All BD to Fill', 'all_to_fill()', icon = os.path.join(BDA_path, "icon/bda_icon_3.png"), index=0)

## Add all_to_fill() to the Toolset
BDA_appearance_menu.addCommand('All BD to Border', 'all_to_border()', icon = os.path.join(BDA_path, "icon/bda_icon_3.png"), index=1)

## Add all_to_fill() to the Toolset
BDA_appearance_menu.addCommand('Selected BD to Fill', 'sel_to_fill()', icon = os.path.join(BDA_path, "icon/bda_icon_3.png"), index=2)

## Add all_to_fill() to the Toolset
BDA_appearance_menu.addCommand('Selected BD to Border', 'sel_to_border()', icon = os.path.join(BDA_path, "icon/bda_icon_3.png"), index=3)

BDA_advenced_menu = BDA_menu.addMenu('Advanced', icon='Modify.png', index=4)

## Add convertToNativeBD to the Advanced menu
BDA_advenced_menu.addCommand('Convert BackdropAdjust to BackdropNode', 'Backdrop_Adjust_advanced.convertToNativeBD()', index=1)

## Add convertToBDAdjust to the Advanced menu
BDA_advenced_menu.addCommand('Convert BackdropNode to BackdropAdjust', 'Backdrop_Adjust_advanced.convertToBDAdjust()', index=2)
