def create_BD_Adj():
    node_xpos = []
    node_ypos = []
    z_List = []
    corner_x = []
    corner_y = []
    corner_bottom = []
    if nuke.selectedNodes('BackdropNode'):
        sel_bd = nuke.selectedNodes('BackdropNode')
        for s in sel_bd:
            corner_x.append(s['xpos'].value() + s['bdwidth'].value())
            corner_y.append(s['ypos'].value())
            corner_bottom.append(s['ypos'].value() + s['bdheight'].value())
            z_List.append(s['z_order'].value())
        else:
            pass

    if nuke.selectedNodes():
        for s in nuke.selectedNodes():
            node_xpos.append(s['xpos'].value())
            node_ypos.append(s['ypos'].value())

        x_max = max(node_xpos + corner_x)
        x_min = min(node_xpos)

        x_width = (float(x_max) - float(min(node_xpos + corner_x)))

        y_max = max(node_ypos)
        y_min = min(node_ypos)

        if not corner_bottom:
            corner_bottom.append(y_max - 1.0)
        cornerYMax = max(corner_bottom)

        if cornerYMax > y_max:
            extra_y = abs((float(y_max) - float(cornerYMax)))
        else:
            extra_y = 0

        y_height = abs((float(min(node_ypos + corner_y)) - float(y_max)))

        if not corner_x:
            corner_x.append(x_max - 1.0)
        cornerXMin = min(corner_x)
        xMax = max(node_xpos)


        #TODO fix extra val to be a dynamic value
        if cornerXMin < xMax:
            extra_val = 80
        else:
            extra_val = 0

        if not z_List:
            z_List.append(0)
        z_Min = min(z_List)

        bd_this = nuke.nodes.Backdrop_Adjust()

        bd_this.setXpos(int(x_min) - 100)
        bd_this['bdwidth'].setValue(x_width + extra_val + 200)
        bd_this.setYpos(int(y_min) - 200)
        bd_this['bdheight'].setValue(y_height + extra_y + 300)
        bd_this['z_order'].setValue(z_Min - 1)

        # Handle tile_color:
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
