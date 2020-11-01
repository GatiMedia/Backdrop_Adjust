def create_BD_Adj():
    node_Xpos = []
    node_Ypos = []
    z_List = []
    if nuke.selectedNodes():
        for s in nuke.selectedNodes():
            try:
                node_Xpos.append(s['xpos'].value())
                node_Ypos.append(s['ypos'].value())
                z_list.append(s['z_order'].value())
            except:
                pass

        x_Max = max(node_Xpos)
        x_Min = min(node_Xpos)

        x_Width = (float(x_Max) - float(x_Min))

        y_Max = max(node_Ypos)
        y_Min = min(node_Ypos)

        y_Height = (float(y_Max) - float(y_Min))

        #TODO fix empty list problem
        if not z_List:
            z_List.append(0)
        z_Min = min(z_List)

        #TODO add darker tile color part

        bd_this = nuke.createNode('Backdrop_Adjust')

        bd_this.setXpos(int(x_Min) - 100)
        bd_this['bdwidth'].setValue(x_Width + 300)
        bd_this.setYpos(int(y_Min) - 200)
        bd_this['bdheight'].setValue(y_Height + 300)
        bd_this['z_order'].setValue(z_Min - 1)
        bd_this.hideControlPanel()
    else:
        bd_that = nuke.createNode('Backdrop_Adjust')
        bd_that['tile_color'].setValue(1717987071)
        bd_that['z_order'].setValue(0)
        bd_that.hideControlPanel()


nuke.menu('Nodes').addMenu('Other').addCommand('BackdropAdjust.', 'create_BD_Adj()', shortcut='ctrl+b', icon='Backdrop.png', index=3)
