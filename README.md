#GM_Backdrop_Adjust

HOW TO INSTALL:
1. Unzip the archive
  
2. Drag and drop the folder in your .nuke folder

[How to find your .nuke folder](https://support.foundry.com/hc/en-us/articles/207271649-Q100048-Nuke-Directory-Locations)

3. Add this code to your file init.py (if you don’t have it, create one) and modify the Backdrop_path.

Backdrop_path = """<path to your .nuke folder>/Backdrop_Adjust/"""
nuke.pluginAddPath(Backdrop_path)

4. Run Nuke
