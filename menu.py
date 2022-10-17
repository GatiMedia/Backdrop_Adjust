#encoding=utf-8
# --------------------------------------------------------------
#  BackdropAdjust menu.py
#  Version: 1.6
#  Last Updated: 12/09/2022
# --------------------------------------------------------------


## Imports
import nuke
import colorsys
import webbrowser

## Z_order from https://learn.foundry.com/nuke/developers/120/pythonreference/nukescripts.autobackdrop-pysrc.html
def zOrderFoundry(node):

    sel_bd = nuke.selectedNodes('BackdropNode')
    def nodeIsInside(node, backdropNode):
        """Returns true if node geometry is inside backdropNode otherwise returns false"""
        topLeftNode = [node.xpos(), node.ypos()]
        topLeftBackDrop = [backdropNode.xpos(), backdropNode.ypos()]
        bottomRightNode = [node.xpos() + node.screenWidth(), node.ypos() + node.screenHeight()]
        bottomRightBackdrop = [backdropNode.xpos() + backdropNode.screenWidth(),
                               backdropNode.ypos() + backdropNode.screenHeight()]

        topLeft = (topLeftNode[0] >= topLeftBackDrop[0]) and (topLeftNode[1] >= topLeftBackDrop[1])
        bottomRight = (bottomRightNode[0] <= bottomRightBackdrop[0]) and (bottomRightNode[1] <= bottomRightBackdrop[1])

        return topLeft and bottomRight

    zOrderF = 0
    # if there are backdropNodes selected put the new one immediately behind the farthest one
    if len(sel_bd):
        zOrderF = min([node.knob("z_order").value() for node in sel_bd]) - 1
    else:
        # otherwise (no backdrop in selection) find the nearest backdrop if exists and set the new one in front of it
        nonSelectedBackdropNodes = nuke.allNodes("BackdropNode")
        for nonBackdrop in nodes:
            for backdrop in nonSelectedBackdropNodes:
                if nodeIsInside(nonBackdrop, backdrop):
                    zOrderF = max(zOrderF, backdrop.knob("z_order").value() + 1)
    return (zOrderF)


def zOrderAlt(node):
    zOrderA = node["bdwidth"].getValue() * node["bdheight"].getValue() * -1
    return (zOrderA)

## The main function
def create_BD_Adj():
    if nuke.selectedNodes():
        sel_bd = nuke.selectedNodes('BackdropNode')
        nodes = nuke.selectedNodes()

        # Calculate bounds for the backdrop node.
        bdX = min([node.xpos() for node in nodes])
        bdY = min([node.ypos() for node in nodes])
        bdW = max([node.xpos() + node.screenWidth() for node in nodes]) - bdX
        bdH = max([node.ypos() + node.screenHeight() for node in nodes]) - bdY

        # Expand the bounds to leave a little border. Elements are offsets for left, top, right and bottom edges respectively
        left, top, right, bottom = (-100, -200, 100, 100)
        bdX += left
        bdY += top
        bdW += (right - left)
        bdH += (bottom - top)

        # Creating the node
        bd_this = nuke.nodes.Backdrop_Adjust()
        bd_this["xpos"].setValue(bdX)
        bd_this["bdwidth"].setValue(bdW)
        bd_this["ypos"].setValue(bdY)
        bd_this["bdheight"].setValue(bdH)

        # z_order Foundry
        if sel_bd:
            bd_this['z_order'].setValue(zOrderFoundry(bd_this))
        else:
            bd_this['z_order'].setValue(0)

        # z_order Alt
        # if nuke.selectedNodes('BackdropNode'):
        #     bd_this['z_order'].setValue(zOrderAlt(bd_this))
        # else:
        #     bd_this['z_order'].setValue(0)

        # For color changing to get luma value
        def tile_luma(node_name):
            # getting tile_color value
            dec_til = nuke.toNode(node_name)['tile_color'].value()
            # dec to hex
            hex_til = hex(dec_til)[2:8]
            # hex to RGB
            rgb = tuple(int(hex_til[i:i + 2], 16) for i in (0, 2, 4))
            # rgb to hls
            (h, l, s) = colorsys.rgb_to_hls(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)
            return (h, l, s)

        # Making tile_color darker than darkest selected BackdropNode's
        if nuke.selectedNodes('BackdropNode'):
            luma_values = []
            node_names = []
            for i in nuke.selectedNodes('BackdropNode'):
                luma_values.append(tile_luma(i.name())[1])
                node_names.append(i.name())

            min_val = (min(luma_values))
            min_val_index = (luma_values.index(min_val))

            min_node_name = (node_names[min_val_index])

            (h, l, s) = (tile_luma(min_node_name))

            # adjust luma value
            l = min_val - .025
            # hls to rgb with clamped luma
            (r, g, b) = colorsys.hls_to_rgb(h, max(min(l, .8), .08), s)
            # rgb to hex
            new_hex = '%02x%02x%02x' % (int(r * 255.0), int(g * 255.0), int(b * 255.0))
            # hex to decimal
            nukeHex = int(new_hex + "00", 16)
            # applying new tile_color
            bd_this['tile_color'].setValue(nukeHex)
        else:
            bd_this['tile_color'].setValue(1717987071)

        bd_this.showControlPanel()
    else:
        #bd_that = nuke.createNode('Backdrop_Adjust')
        bd_that = nuke.createNode('Backdrop_Adjust')
        bd_that['tile_color'].setValue(1717987071)
        # z_order Foundry
        bd_that['z_order'].setValue(0)
        # z_order Alt
        #bd_that['z_order'].setValue(-250000)
        bd_that.showControlPanel()

## Add to the Toolset
nuke.menu('Nodes').addMenu('Other').addCommand('BackdropAdjust', 'create_BD_Adj()', shortcut='Shift+b', icon='Backdrop.png', index=3)

## Cover selected nodes' area
def coverSelectedArea():
    bd_this = nuke.thisNode()
    if nuke.selectedNodes():

        nodes = nuke.selectedNodes()

        # Calculate bounds for the backdrop node.
        bdX = min([node.xpos() for node in nodes])
        bdY = min([node.ypos() for node in nodes])
        bdW = max([node.xpos() + node.screenWidth() for node in nodes]) - bdX
        bdH = max([node.ypos() + node.screenHeight() for node in nodes]) - bdY

        # Expand the bounds to leave a little border. Elements are offsets for left, top, right and bottom edges respectively
        left, top, right, bottom = (-100, -200, 100, 100)
        bdX += left
        bdY += top
        bdW += (right - left)
        bdH += (bottom - top)

        # Applying the values
        bd_this["xpos"].setValue(bdX)
        bd_this["bdwidth"].setValue(bdW)
        bd_this["ypos"].setValue(bdY)
        bd_this["bdheight"].setValue(bdH)
        
        # Select the BD node along with the already selected nodes so can grab and move easier
        bd_this.setSelected(True)

        # z_order Foundry
        if nuke.selectedNodes('BackdropNode'):
            bd_this['z_order'].setValue(zOrderFoundry(bd_this))
        else:
            pass

        # z_order Alt
        # if nuke.selectedNodes('BackdropNode'):
        #     bd_this['z_order'].setValue(zOrderAlt(bd_this))
        # else:
        #     bd_this['z_order'].setValue(0)

    else:
        nuke.message('<font color=orange><b>\n\nSelect some nodes first!\n\n')

## Extend selected nodes' area
def extendSelectedArea():
    bd_this = nuke.thisNode()
    if nuke.selectedNodes():
        nodes = nuke.selectedNodes()

        # Calculate bounds for the backdrop node.
        bdX = min([node.xpos() for node in nodes])
        bdY = min([node.ypos() for node in nodes])
        bdW = max([node.xpos() + node.screenWidth() for node in nodes]) - bdX
        bdH = max([node.ypos() + node.screenHeight() for node in nodes]) - bdY

        # Expand the bounds to leave a little border. Elements are offsets for left, top, right and bottom edges respectively
        left, top, right, bottom = (-100, -200, 100, 100)
        bdX += left
        bdY += top
        bdW += (right - left)
        bdH += (bottom - top)

        # Applying the values
        if bd_this['xpos'].value() > (bdX):
            bd_this["bdwidth"].setValue(bd_this['bdwidth'].value() + (bd_this['xpos'].value() - bdX))
            bd_this["xpos"].setValue(bdX)
        if bd_this['ypos'].value() > (bdY):
            bd_this["bdheight"].setValue(bd_this['bdheight'].value() + (bd_this['ypos'].value() - bdY))
            bd_this["ypos"].setValue(bdY)
        if (bd_this['xpos'].value() + bd_this['bdwidth'].value()) < (bdW + bdX):
            relW = (bdW + bdX)
            rel_thisW = int(bd_this['xpos'].value()) + int(bd_this['bdwidth'].value())
            bd_this["bdwidth"].setValue(bd_this['bdwidth'].value() + (relW - rel_thisW))
        if (bd_this['ypos'].value() + bd_this['bdheight'].value()) < (bdH + bdY):
            relH = (bdH + bdY)
            rel_thisH = int(bd_this['ypos'].value()) + int(bd_this['bdheight'].value())
            bd_this["bdheight"].setValue(bd_this['bdheight'].value() + (relH - rel_thisH))
        
        # Selecting the BD node and the ones already on it along with the already selected ones so can grab and move easier
        for n in bd_this.getNodes():
            n.setSelected(True)
        bd_this.setSelected(True)

        # z_order Foundry
        if nuke.selectedNodes('BackdropNode'):
            bd_this['z_order'].setValue(zOrderFoundry(bd_this))
        else:
            pass

        # z_order Alt
        # if nuke.selectedNodes('BackdropNode'):
        #     bd_this['z_order'].setValue(zOrderAlt(bd_this))
        # else:
        #     bd_this['z_order'].setValue(0)

    else:
        nuke.message('<font color=orange><b>\n\nSelect some nodes first!\n\n')


def fontPlusTen():
    curr_size = nuke.thisNode()['note_font_size'].value()
    nuke.thisNode()['note_font_size'].setValue(curr_size + 10)


def fontMinusTen():
    curr_size = nuke.thisNode()['note_font_size'].value()
    nuke.thisNode()['note_font_size'].setValue(curr_size - 10)

## Vivid/Dull palette knob
def dullVividColor():
    dull = '<big><font style="background-color:#806060;">D<font style="background-color:#807460;">u<font style="background-color:#778060;">l<font style="background-color:#608071;">l<font style="background-color:#607a80;"> <font style="background-color:#606680;">C<font style="background-color:#606680;">o<font style="background-color:#6d6080;">l<font style="background-color:#80607d;">o<font style="background-color:#806069;">r<font style="background-color:#806060;">s'

    vivid = '<big><font style="background-color:#994d4d;">V<font style="background-color:#997d4d;">i<font style="background-color:#85994d;">v<font style="background-color:#55994d;">i<font style="background-color:#4d9976;">d<font style="background-color:#4d8c99;"> <font style="background-color:#4d5c99;">C<font style="background-color:#6e4d99;">o<font style="background-color:#994d94;">l<font style="background-color:#994d63;">o<font style="background-color:#994d4d;">r<font style="background-color:#997d4d;">s'

    knob = nuke.thisKnob()
    node = nuke.thisNode()
    options = [dull, vivid]
    knob.setLabel(options[int(knob.label() == options[0])])

    dull_colors = ['2153799680', '2155110400', '2004901888', '1669357568', '1619030272', '1618640896', '1617330176',
                   '1835040768', '2153807104', '2153801984']

    dull_colors_hex = ['806060', '807460', '778060', '638060', '608071', '607a80', '606680', '6d6080', '80607d',
                       '806069']

    vivid_colors = ['2571980032', '2575125760', '2241416448', '1436110080', '1301902848', '1301059840', '1297914112',
                    '1850579200', '2571998208', '2571985664']

    vivid_colors_hex = ['994d4d', '997d4d', '85994d', '55994d', '4d9976', '4d8c99', '4d5c99', '6e4d99', '994d94',
                        '994d63']

    knob_names = ["color_{}".format(x) for x in range(10)]

    if knob.label() == dull:
        items = zip(dull_colors, dull_colors_hex)
    else:
        items = zip(vivid_colors, vivid_colors_hex)

    for i, (color, hex_color) in enumerate(items):
        node[knob_names[i]].setLabel("<font color=#{}><big>█</big></font>".format(hex_color))
        node[knob_names[i]].setValue("nuke.thisNode()['tile_color'].setValue({})".format(color))

## Darken tile_color
def darkenTileColor():
    # getting tile_color value
    dec_til = nuke.thisNode()['tile_color'].value()

    # dec to hex
    hex_til = hex(dec_til)[2:8]

    # hex to RGB
    rgb = tuple(int(hex_til[i:i + 2], 16) for i in (0, 2, 4))

    # rgb to hls
    (h, l, s) = colorsys.rgb_to_hls(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)

    # adjust luma value
    l = l - .025

    # hls to rgb with clamped luma
    (r, g, b) = colorsys.hls_to_rgb(h, max(min(l, .8), .08), s)

    # rgb to hex
    new_hex = '%02x%02x%02x' % (int(r * 255.0), int(g * 255.0), int(b * 255.0))

    # hex to decimal
    nukeHex = int(new_hex + "00", 16)

    # applying new tile_color
    nuke.thisNode()['tile_color'].setValue(nukeHex)

## Brighten tile_color
def brightenTileColor():
    # getting tile_color value
    dec_til = nuke.thisNode()['tile_color'].value()

    # dec to hex
    hex_til = hex(dec_til)[2:8]

    # hex to RGB
    rgb = tuple(int(hex_til[i:i + 2], 16) for i in (0, 2, 4))

    # rgb to hls
    (h, l, s) = colorsys.rgb_to_hls(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)

    # adjust luma value
    l = l + .025

    # hls to rgb with clamped luma
    (r, g, b) = colorsys.hls_to_rgb(h, max(min(l, .8), .08), s)

    # rgb to hex
    new_hex = '%02x%02x%02x' % (int(r * 255.0), int(g * 255.0), int(b * 255.0))

    # hex to decimal
    nukeHex = int(new_hex + "00", 16)

    # applying new tile_color
    nuke.thisNode()['tile_color'].setValue(nukeHex)


def addY100():
    bd_this = nuke.thisNode()
    bd_this['bdheight'].setValue(int(bd_this['bdheight'].value()) + 100)

    # z_order Foundry
    if nuke.selectedNodes('BackdropNode'):
        bd_this['z_order'].setValue(zOrderFoundry(bd_this))
    else:
        pass

    # z_order Alt
    # if nuke.selectedNodes('BackdropNode'):
    #     bd_this['z_order'].setValue(zOrderAlt(bd_this))
    # else:
    #     bd_this['z_order'].setValue(0)


def addY500():
    bd_this = nuke.thisNode()
    bd_this['bdheight'].setValue(int(bd_this['bdheight'].value()) + 500)

    # z_order Foundry
    if nuke.selectedNodes('BackdropNode'):
        bd_this['z_order'].setValue(zOrderFoundry(bd_this))
    else:
        pass

    # z_order Alt
    # if nuke.selectedNodes('BackdropNode'):
    #     bd_this['z_order'].setValue(zOrderAlt(bd_this))
    # else:
    #     bd_this['z_order'].setValue(0)


def takeY100():
    bd_this = nuke.thisNode()
    bd_this['bdheight'].setValue(int(bd_this['bdheight'].value()) - 100)

    # z_order Foundry
    if nuke.selectedNodes('BackdropNode'):
        bd_this['z_order'].setValue(zOrderFoundry(bd_this))
    else:
        pass

    # z_order Alt
    # if nuke.selectedNodes('BackdropNode'):
    #     bd_this['z_order'].setValue(zOrderAlt(bd_this))
    # else:
    #     bd_this['z_order'].setValue(0)


def takeY500():
    bd_this = nuke.thisNode()
    bd_this['bdheight'].setValue(int(bd_this['bdheight'].value()) - 500)

    # z_order Foundry
    if nuke.selectedNodes('BackdropNode'):
        bd_this['z_order'].setValue(zOrderFoundry(bd_this))
    else:
        pass

    # z_order Alt
    # if nuke.selectedNodes('BackdropNode'):
    #     bd_this['z_order'].setValue(zOrderAlt(bd_this))
    # else:
    #     bd_this['z_order'].setValue(0)


def addX100():
    bd_this = nuke.thisNode()
    bd_this['bdwidth'].setValue(int(bd_this['bdwidth'].value()) + 100)

    # z_order Foundry
    if nuke.selectedNodes('BackdropNode'):
        bd_this['z_order'].setValue(zOrderFoundry(bd_this))
    else:
        pass

    # z_order Alt
    # if nuke.selectedNodes('BackdropNode'):
    #     bd_this['z_order'].setValue(zOrderAlt(bd_this))
    # else:
    #     bd_this['z_order'].setValue(0)


def addX500():
    bd_this = nuke.thisNode()
    bd_this['bdwidth'].setValue(int(bd_this['bdwidth'].value()) + 500)

    # z_order Foundry
    if nuke.selectedNodes('BackdropNode'):
        bd_this['z_order'].setValue(zOrderFoundry(bd_this))
    else:
        pass

    # z_order Alt
    # if nuke.selectedNodes('BackdropNode'):
    #     bd_this['z_order'].setValue(zOrderAlt(bd_this))
    # else:
    #     bd_this['z_order'].setValue(0)


def takeX100():
    bd_this = nuke.thisNode()
    bd_this['bdwidth'].setValue(int(bd_this['bdwidth'].value()) - 100)

    # z_order Foundry
    if nuke.selectedNodes('BackdropNode'):
        bd_this['z_order'].setValue(zOrderFoundry(bd_this))
    else:
        pass

    # z_order Alt
    # if nuke.selectedNodes('BackdropNode'):
    #     bd_this['z_order'].setValue(zOrderAlt(bd_this))
    # else:
    #     bd_this['z_order'].setValue(0)


def takeX500():
    bd_this = nuke.thisNode()
    bd_this['bdwidth'].setValue(int(bd_this['bdwidth'].value()) - 500)

    # z_order Foundry
    if nuke.selectedNodes('BackdropNode'):
        bd_this['z_order'].setValue(zOrderFoundry(bd_this))
    else:
        pass

    # z_order Alt
    # if nuke.selectedNodes('BackdropNode'):
    #     bd_this['z_order'].setValue(zOrderAlt(bd_this))
    # else:
    #     bd_this['z_order'].setValue(0)

def openWebsite():
    webbrowser.open('https://www.gatimedia.co.uk/backdrop-adjust', new=2)
