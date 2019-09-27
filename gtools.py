import bpy
from bpy.types import (
    AddonPreferences,
    Operator,
    Panel,
    PropertyGroup,
)
from bpy.props import (IntProperty)
from bpy.props import (BoolProperty)


bl_info = {
    "name" : "GameTools",
    "author" : "Slipher3D",
    "description" : "Applies bevel, subsurf modifiers and smooths the mesh.",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 2),
    "location" : "",
    "warning" : "",
    "category" : "Object"
}


class AddBevelAndSubDiv(bpy.types.Operator):
    """Add Bevel and SubSurf Mods"""
    bl_idname = "object.bsd"
    bl_label = "Add Bevel and SubSurf"
    bl_description = "Adds bevel and subsurf modifiers"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'REGISTER', 'UNDO'}

    sublevel: bpy.props.IntProperty(name="SubSurf Level", default = 3, min = 1, description="sub levels")
    viewapply: bpy.props.BoolProperty(name="View SubSurf Level", default = True, description="view sub levels")
    smoothapply: bpy.props.BoolProperty(name = "Smooth object", default = True, description = "apply smoothing to mesh")

    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type == 'MESH'

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        for ob in bpy.context.selected_objects:
            bpy.context.view_layer.objects.active = ob
            bpy.ops.object.editmode_toggle()
            if self.smoothapply is True:
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.faces_shade_smooth()
            else:
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.faces_shade_flat()
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.modifier_add(type='BEVEL')
            bpy.context.object.modifiers["Bevel"].limit_method = 'WEIGHT'
            bpy.ops.object.modifier_add(type='SUBSURF')
            if self.viewapply is True:
                bpy.context.object.modifiers["Subdivision"].levels = self.sublevel
            bpy.context.object.modifiers["Subdivision"].render_levels = self.sublevel

        return {'FINISHED'}
 
def menu_func(self, context):
    self.layout.Operator(AddBevelAndSubDiv.bl_idname)


def register():
    bpy.utils.register_class(AddBevelAndSubDiv)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(AddBevelAndSubDiv)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()
