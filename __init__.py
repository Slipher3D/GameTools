bl_info = {
    "name" : "GameTools",
    "author" : "Slipher3D",
    "description" : "Applies bevel, subsurf modifiers and smooths the mesh.",
    "blender" : (2, 80, 0),
    "version" : (0, 2, 0),
    "location" : "",
    "warning" : "",
    "category" : "Object"
}


import bpy

from . gtools import BevelSubSurf_OT_Operator
from . gtools import MO_Renamer_OT_Operator
from . gtools_panel import Gtools_PT_Panel

classes = (BevelSubSurf_OT_Operator, Gtools_PT_Panel, MO_Renamer_OT_Operator)

register, unregister = bpy.utils.register_classes_factory(classes)