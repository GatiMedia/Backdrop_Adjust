def create_BD_Adj():
    node_Xpos = []
    node_Ypos = []
    z_List = []
    if nuke.selectedNodes():
        for s in nuke.selectedNodes():
            try:
                node_Xpos.append(s['xpos'].value())
                node_Ypos.append(s['ypos'].value())
                z_List.append(s['z_order'].value())
            except:
                pass

        x_Max = max(node_Xpos)
        x_Min = min(node_Xpos)

        x_Width = (float(x_Max) - float(x_Min))

        y_Max = max(node_Ypos)
        y_Min = min(node_Ypos)

        y_Height = (float(y_Max) - float(y_Min))

        if not z_List:
            z_List.append(0)
        z_Min = min(z_List)

        bd_this = nuke.nodes.Backdrop_Adjust()

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

        #TODO fix size issue

        bd_this.setXpos(int(x_Min) - 100)
        bd_this['bdwidth'].setValue(x_Width + 300)
        bd_this.setYpos(int(y_Min) - 200)
        bd_this['bdheight'].setValue(y_Height + 300)
        bd_this['z_order'].setValue(z_Min - 1)
        bd_this.hideControlPanel()
    else:
        bd_that = nuke.createNode('Backdrop_Adjust')
        bd_that['tile_color'].setValue(3149642751)
        bd_that['z_order'].setValue(0)
        bd_that.hideControlPanel()


nuke.menu('Nodes').addMenu('Other').addCommand('BackdropAdjust.', 'create_BD_Adj()', shortcut='ctrl+b', icon='Backdrop.png', index=3)
