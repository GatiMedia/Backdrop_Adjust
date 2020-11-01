### MODIFY TILE COLOR ###

color_list = []

for s in nuke.selectedNodes('BackdropNode'):
    try:
        color_list.append(s['tile_color'].value())
    except:
        pass

dec_til = min(color_list)

# Dec to Hex
hex_til = hex(int(dec_til))

# Hex strip
hex_til_to_rgb = hex_til[2:8]

# Hex to RGB
rgb_til = tuple(int(hex_til_to_rgb[i:i+2], 16) for i in (0, 2, 4))

rgb_til_list = list(rgb_til)

# Modifying RGB to a new value
rgb_til_list_new = []
for i in rgb_til_list:
    rgb_til_list_new.append(i - 30)

# Preventing minus values
for n, i in enumerate(rgb_til_list_new):
   if i < 0:
      rgb_til_list_new[n] = 1

# RGB to Hex
new_hex = ('%02x%02x%02x' % (rgb_til_list_new[0], rgb_til_list_new[1], rgb_til_list_new[2])) + '00'

# Hex to Dec
new_dec = int(new_hex, 16)

nuke.toNode('BackdropNode9')['tile_color'].setValue(int(new_dec))


print (dec_til)
print (hex_til)
print (rgb_til_list_new)
print (new_dec)
