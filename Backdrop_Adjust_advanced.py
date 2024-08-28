#encoding=utf-8
# --------------------------------------------------------------
#  Backdrop_Adjust_advanced.py
#  Version: 2.0
#  Last Updated: 27/08/2024
#  Last updated by: Attila Gasparetz
# --------------------------------------------------------------

## Imports
import nuke

def convertToNativeBD():
    sel_nodes = nuke.selectedNodes()
    if len(sel_nodes) < 1:
        nuke.message("""<center><font color=orange>Select a single or multiple Bakcdrop_Adjust first!""")
    else:
        for n in sel_nodes:
            if n.Class() == "BackdropNode":
                if "Backdrop_Adjust" in n.name():
                    note_val = n['note'].value()
                    note_color_val = n['note_color'].value()
                    note_align_val = n['align'].value()
                    note_bold_val = n['bold'].value()
                    note_italian_val = n['italian'].value()
                    note_under_val = n['under'].value()
                    note_strike_val = n['strike'].value()

                    note_size_val = n['note_font_size'].value()

                    note_tile_color_val = n['tile_color'].value()
                    node_appearance_val = n['appearance'].value()

                    node_z_order_val = n['z_order'].value()

                    node_xpos_val = n['xpos'].value()
                    node_ypos_val = n['ypos'].value()
                    node_bdwidth_val = n['bdwidth'].value()
                    node_bdheight_val = n['bdheight'].value()

                    nuke.delete(n)

                    new_bd = nuke.nodes.BackdropNode()
                    new_bd['label'].setValue("""<p align="%s"><font color=%s>""" % (note_align_val, note_color_val))

                    if note_bold_val == True:
                        new_bd['label'].setValue(new_bd['label'].value() + str("<b>"))

                    if note_italian_val == True:
                        new_bd['label'].setValue(new_bd['label'].value() + str("<i>"))

                    if note_under_val == True:
                        new_bd['label'].setValue(new_bd['label'].value() + str("<u>"))

                    if note_strike_val == True:
                        new_bd['label'].setValue(new_bd['label'].value() + str("<s>"))

                    new_bd['label'].setValue(new_bd['label'].value() + str(note_val))

                    new_bd['note_font_size'].setValue(note_size_val)

                    new_bd['tile_color'].setValue(note_tile_color_val)
                    new_bd['appearance'].setValue(node_appearance_val)
                    new_bd['z_order'].setValue(node_z_order_val)

                    new_bd['xpos'].setValue(node_xpos_val)
                    new_bd['ypos'].setValue(node_ypos_val)
                    new_bd['bdwidth'].setValue(node_bdwidth_val)
                    new_bd['bdheight'].setValue(node_bdheight_val)



def convertToBDAdjust():
    sel_nodes = nuke.selectedNodes()
    if len(sel_nodes) < 1:
        nuke.message("""<center><font color=orange>Select a single or multiple BakcdropNode first!""")
    else:
        for n in sel_nodes:
            if n.Class() == "BackdropNode":
                if not "Backdrop_Adjust" in n.name():
                    label_val = n['label'].value()

                    note_size_val = n['note_font_size'].value()

                    note_tile_color_val = n['tile_color'].value()
                    node_appearance_val = n['appearance'].value()

                    node_z_order_val = n['z_order'].value()

                    node_xpos_val = n['xpos'].value()
                    node_ypos_val = n['ypos'].value()
                    node_bdwidth_val = n['bdwidth'].value()
                    node_bdheight_val = n['bdheight'].value()

                    nuke.delete(n)

                    new_bd = nuke.nodes.Backdrop_Adjust()
                    new_bd['note'].setValue(label_val)

                    new_bd['note_font_size'].setValue(note_size_val)

                    new_bd['tile_color'].setValue(note_tile_color_val)
                    new_bd['appearance'].setValue(node_appearance_val)
                    new_bd['z_order'].setValue(node_z_order_val)

                    new_bd['xpos'].setValue(node_xpos_val)
                    new_bd['ypos'].setValue(node_ypos_val)
                    new_bd['bdwidth'].setValue(node_bdwidth_val)
                    new_bd['bdheight'].setValue(node_bdheight_val)
