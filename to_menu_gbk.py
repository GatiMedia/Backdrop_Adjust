def create_BD_Adj():
    import colorsys
    z_List = []
    if nuke.selectedNodes():

        if nuke.selectedNodes('BackdropNode'):
            sel_bd = nuke.selectedNodes('BackdropNode')
            for s in sel_bd:
                z_List.append(s['z_order'].value())
            else:
                pass

        if not z_List:
            z_List.append(1)
        z_Min = min(z_List)
        
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
        #bd_this['z_order'].setValue(z_Min - 1)

        # GBK BD size method
        bd_this['z_order'].setValue(bdW * bdH * -1)

        def tile_luma(node_name):
            # getting tile_color value
            dec_til = nuke.toNode(node_name)['tile_color'].value()
            # dec to hex
            hex_til = hex(dec_til)[2:8]
            # hex to RGB
            rgb = tuple(int(hex_til[i:i + 2], 16) for i in (0, 2, 4))
            # rgb to hls
            (h, l, s) = colorsys.rgb_to_hls(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
            return (h, l, s)

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
            new_hex = '%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))
            # hex to decimal
            nukeHex = int(new_hex + "00", 16)
            # applying new tile_color
            bd_this['tile_color'].setValue(nukeHex)
        else:
            bd_this['tile_color'].setValue(1717987071)

        bd_this.showControlPanel()
    else:
        bd_that = nuke.createNode('Backdrop_Adjust')
        bd_that['tile_color'].setValue(1717987071)
        bd_that['z_order'].setValue(-250000)
        bd_that.showControlPanel()

nuke.menu('Nodes').addMenu('Other').addCommand('BackdropAdjust.', 'create_BD_Adj()', shortcut='ctrl+b', icon='Backdrop.png', index=3)
