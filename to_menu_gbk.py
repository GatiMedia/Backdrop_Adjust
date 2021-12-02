def create_BD_Adj():
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

        # Handle tile_color by Borsari Nicola
        ok_colors = [3149642751, 2863311615, 2576980479, 2290649343, 2004318207, 1717987071, 1431655935, 1145324799,
                     572662527, 286331391, 255]

        if nuke.selectedNodes('BackdropNode'):
            existing_indexes = [0]
            for bd in nuke.selectedNodes('BackdropNode'):
                color = int(bd['tile_color'].getValue())
                try:
                    curr_index = ok_colors.index(color)
                    existing_indexes.append(curr_index)
                except ValueError:
                    continue

            new_index = sorted(existing_indexes)[-1] + 1

            try:
                bd_this['tile_color'].setValue(ok_colors[new_index])
            except IndexError:
                bd_this['tile_color'].setValue(ok_colors[-1])
        else:
            bd_this['tile_color'].setValue(3149642751)

        bd_this.showControlPanel()
    else:
        bd_that = nuke.createNode('Backdrop_Adjust')
        bd_that['tile_color'].setValue(3149642751)
        bd_that['z_order'].setValue(-250000)
        bd_that.showControlPanel()

nuke.menu('Nodes').addMenu('Other').addCommand('BackdropAdjust.', 'create_BD_Adj()', shortcut='ctrl+b', icon='Backdrop.png', index=3)
