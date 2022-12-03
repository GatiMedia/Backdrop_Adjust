#GM_Backdrop_Adjust

LAST UPDATE: 03/12/2022

CURRENT VERSION: 1.8

HOW TO INSTALL:
1. Unzip the archive
  
2. Drag and drop the folder in your .nuke folder

[How to find your .nuke folder](https://support.foundry.com/hc/en-us/articles/207271649-Q100048-Nuke-Directory-Locations)

3. Make sure your folder is called **Backdrop_Adjust** ( You might need to rename it )

4. Add this code to your file init.py (if you don’t have it, create one) and modify the Backdrop_path.

```python
Backdrop_path = """<path to your .nuke folder>/Backdrop_Adjust/"""
nuke.pluginAddPath(Backdrop_path)
```

5. Run Nuke
