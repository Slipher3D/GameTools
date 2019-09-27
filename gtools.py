import bpy
from bpy.types import (
    AddonPreferences,
    Operator,
    PropertyGroup,
)
from bpy.props import (IntProperty)
from bpy.props import (BoolProperty)
from . gtools_panel import Gtools_PT_Panel

class BevelSubSurf_OT_Operator(bpy.types.Operator):
    """Add Bevel and SubSurf Mods"""
    bl_idname = "object.bsd"
    bl_label = "Add Bevel and SubSurf"
    bl_description = "Adds bevel and subsurf modifiers"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'REGISTER', 'UNDO'}

    sublevel: bpy.props.IntProperty(name = "SubSurf Level Render", default = 3, min = 1, description="apply sub levels to render")
    viewapply: bpy.props.BoolProperty(name = "Apply SubSurf Level to View", default = True, description="apply sub levels to view")
    smoothapply: bpy.props.BoolProperty(name = "Smooth Mesh", default = True, description = "apply smoothing to mesh")

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

class MO_Renamer_OT_Operator(bpy.types.Operator):
    """"Object Rename Appender"""
    bl_idname = 'object.morenamer'
    bl_label = 'Rename Selection'
    bl_options = {'REGISTER', 'UNDO'}

    name: bpy.props.StringProperty(name = "Name", default = "")
    prefix: bpy.props.StringProperty(name = "Prefix", default = "")
    suffix: bpy.props.StringProperty(name = "Suffix", default = "")

    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type == 'MESH'

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        
        sObjs = bpy.context.selected_objects

        if not self.name:

            for o in sObjs:
                on = o.name
                o.name = on + self.suffix
                on = o.name
                o.name = self.prefix + on

        else:
            for o in sObjs:
                o.name = self.name
                on = o.name
                o.name = on + self.suffix
                on = o.name
                o.name = self.prefix + on

        return {'FINISHED'}