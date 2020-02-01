# GameTools
An addon for Blender 2.8 to assist in game asset creation.

This addon is centered around making tedious tasks quicker for baking and exporting. The workflow in mind is exporting from Blender 2.8 to Substance Painter with quick multi-object renaming and exporting based on object name/selection.

Multi-Object Renamer
This tools allows the renaming of the current selection of meshes with prefix, suffix, and enumeration. The enumeration follows that of blender's convention (ie 'meshname'.001).

Export
Export is a quick export menu for exporting meshes for baking. Each mesh can be exported as it's own file, or all together broken up into two files, the low and high. The object list is taken from the currently selected meshes. It currently supports FBX and OBJ, with a limited set of options. 
