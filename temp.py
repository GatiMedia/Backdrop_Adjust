### DARKEN TILE COLOR ###

import colorsys

# getting tile_color value
dec_til = nuke.thisNode()['tile_color'].value()

# dec to hex
hex_til = hex(dec_til)[2:8]

# hex to RGB
rgb = tuple(int(hex_til[i:i+2], 16) for i in (0, 2, 4))

# rgb to hls
(h, l, s) = colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255)

# adjust luma value
l = l - .025

# hls to rgb with clamped luma
(r, g, b) = colorsys.hls_to_rgb(h, max(min(l, .8), .08), s)

# rgb to hex
new_hex = '%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))

# hex to decimal
nukeHex = int(new_hex+"00", 16)

# applying new tile_color
nuke.thisNode()['tile_color'].setValue(nukeHex)
