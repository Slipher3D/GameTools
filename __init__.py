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

from . gtools import MO_Renamer_OT_Operator, GT_Property_Group, LC_Exporter_OT_Operator
from . gtools_panel import Gtools_PT_Panel

classes = (Gtools_PT_Panel, MO_Renamer_OT_Operator, GT_Property_Group, LC_Exporter_OT_Operator)

reg, unreg = bpy.utils.register_classes_factory(classes)

def register():
    reg()
    bpy.types.Scene.custom_props = bpy.props.PointerProperty(type=GT_Property_Group)

def unregister():
    unreg()
    del bpy.types.Scene.custom_props