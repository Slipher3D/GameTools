bl_info = {
    "name" : "GameTools",
    "author" : "Slipher3D",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import bpy


class AddBevelAndSubDiv(bpy.types.Operator):
    """Add Bevel and Sub Div Mods"""
    bl_idname = "object.bsd"
    bl_label = "Add Bevel and SubDiv"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        for ob in bpy.context.selected_objects:
            bpy.context.view_layer.objects.active = ob
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
            bpy.ops.mesh.faces_shade_smooth()
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.modifier_add(type='BEVEL')
            bpy.context.object.modifiers["Bevel"].limit_method = 'WEIGHT'
            bpy.ops.object.modifier_add(type='SUBSURF')
            bpy.context.object.modifiers["Subdivision"].levels = 3

        return {'FINISHED'}
 
def register():
    bpy.utils.register_class(AddBevelAndSubDiv)

def unregister():
    bpy.utils.unregister_class(AddBevelAndSubDiv)

if __name__ == "__main__":
    register()