def create_BD_Adj():
    node_xpos = []
    node_ypos = []
    z_List = []
    bd_xpos = []
    bd_ypos = []
    if nuke.selectedNodes('BackdropNode'):
        sel_bd = nuke.selectedNodes('BackdropNode')
        for s in sel_bd:
            bd_xpos.append(s['xpos'].value())
            bd_xpos.append(s['xpos'].value() + s['bdwidth'].value())
            bd_ypos.append(s['ypos'].value())
            bd_ypos.append(s['ypos'].value() + s['bdheight'].value())
            z_List.append(s['z_order'].value())
        else:
            pass

    if nuke.selectedNodes():
        for s in nuke.selectedNodes():
            node_xpos.append(s['xpos'].value())
            node_ypos.append(s['ypos'].value())

        x_max = max(node_xpos)
        x_min = min(node_xpos)

        y_max = max(node_ypos)
        y_min = min(node_ypos)

        # Calculating the node's size in if the lowest right corner isn't a Backdrop but a node
        if not bd_xpos:
            bd_xpos.append(x_min)
            bd_ypos.append(y_max)

        if bd_xpos:
            max_bd_xpos = max(bd_xpos)
            min_bd_xpos = min(bd_xpos)

            max_bd_ypos = max(bd_ypos)
            min_bd_ypos = min(bd_ypos)

            if max_bd_xpos > x_max:
                x_extra = 0
            else:
                x_extra = 80

            if max_bd_ypos > y_max:
                y_extra = 0
            else:
                y_extra = 30

        else:
            pass

        x_max = max(node_xpos + bd_xpos)
        x_min = min(node_xpos + bd_xpos)

        x_width = (float(x_max) - float(x_min))

        y_max = max(node_ypos + bd_ypos)
        y_min = min(node_ypos + bd_ypos)

        y_height = (float(y_max) - float(y_min))


        if not z_List:
            z_List.append(0)
        z_Min = min(z_List)


        # Creating the node
        bd_this = nuke.nodes.Backdrop_Adjust()

        bd_this.setXpos(int(x_min) - 100)
        bd_this['bdwidth'].setValue(int(x_width) + int(x_extra) + 200)
        bd_this.setYpos(int(y_min) - 200)
        bd_this['bdheight'].setValue(int(y_height) + int(y_extra) + 300)
        bd_this['z_order'].setValue(z_Min - 1)

        # Handle tile_color
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

        bd_this.hideControlPanel()
    else:
        bd_that = nuke.createNode('Backdrop_Adjust')
        bd_that['tile_color'].setValue(3149642751)
        bd_that['z_order'].setValue(0)
        bd_that.hideControlPanel()

nuke.menu('Nodes').addMenu('Other').addCommand('BackdropAdjust.', 'create_BD_Adj()', shortcut='ctrl+b', icon='Backdrop.png', index=3)
