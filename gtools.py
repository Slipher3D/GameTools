import bpy
import os
from bpy.types import (
    AddonPreferences,
    Operator,
    PropertyGroup,
)
from bpy.props import (
    IntProperty, 
    BoolProperty
    )
from . gtools_panel import Gtools_PT_Panel

"""
class BevelSubSurf_OT_Operator(bpy.types.Operator):
    """"""Add Bevel and SubSurf Mods""""""
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
"""

class GT_Property_Group(bpy.types.PropertyGroup):
    #MO_Renamer_PG
    name: bpy.props.StringProperty(name = "Name", default = "")
    prefix: bpy.props.StringProperty(name = "Prefix", default = "")
    suffix: bpy.props.StringProperty(name = "Suffix", default = "")
    startnum: bpy.props.IntProperty(name = "Start Number", default = 1, min = 1)
    usenums: bpy.props.BoolProperty(name = "Enumerate", default = False)
    step: bpy.props.IntProperty(name = "Step", default = 1, min = 1)

    #lcexporter
    fileperobject: bpy.props.BoolProperty(name = "File Per Object", default = False)
    outputpath: bpy.props.StringProperty(name = "Output Path", subtype = 'FILE_PATH')
    filename: bpy.props.StringProperty(name = "File Name", default = "Mesh")
    low_ref: bpy.props.StringProperty(name = "Low", default = "_low")
    high_ref: bpy.props.StringProperty(name = "High", default = "_high")
    export_filetype: bpy.props.EnumProperty(name = "Filetype", description = "Choose filetype for export.", 
    items = [('0', "FBX", ""),
            ('1', "OBJ", "")
    ])
    #FBX Options
    bakeanim: bpy.props.BoolProperty(name = "Bake Animation", default = False)
    applymods: bpy.props.BoolProperty(name = "Apply Mods", default = True)
    smoothing: bpy.props.EnumProperty(name = "Smoothing",
        items = [('OFF', "Off", ""),
                ('FACE', "Edge", ""), 
                ('EDGE', "Face", "")
        ])
    #OBJ Options
    anim: bpy.props.BoolProperty(name = "Animation", default = False)
    smoothingo: bpy.props.BoolProperty(name = "Smoothing", default = True)
    materials: bpy.props.BoolProperty(name = "Write Mats", default = False)
    triangulate: bpy.props.BoolProperty(name = "Triangulate", default = True)
    
class MO_Renamer_OT_Operator(bpy.types.Operator):
    """"Object Rename Appender"""
    bl_idname = 'object.morenamer'
    bl_label = 'Rename Selection'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type == 'MESH'
    
    #def invoke(self, context, event):
    #    return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        
        sObjs = bpy.context.selected_objects
        scene = context.scene
        snum = scene.custom_props.startnum

        #if name == ""
        if not scene.custom_props.name:
            try:
                iter(sObjs)
                for o in sObjs:
                    o.name = scene.custom_props.prefix + o.name + scene.custom_props.suffix
                    if scene.custom_props.usenums:
                        o.name = o.name + "." + str(snum).zfill(3)
                        snum = snum + scene.custom_props.step
            except TypeError:
                print("Not iterable.")

        else:
            try:
                iter(sObjs)
                for o in sObjs:
                    o.name = scene.custom_props.prefix + scene.custom_props.name + scene.custom_props.suffix
                    if scene.custom_props.usenums:
                        o.name = o.name + "." + str(snum).zfill(3)
                        snum = snum + scene.custom_props.step
            except TypeError:
                print("Not iterable.")

        return {'FINISHED'}

class LC_Exporter_OT_Operator(bpy.types.Operator):
    """Lightingcrest Exporter"""
    bl_idname = 'object.lcexporter'
    bl_label =  'Exporter'
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type == 'MESH'

    def execute(self, context):
        scene = context.scene
        sObjs = bpy.context.selected_objects
        lows = []
        highs = []
        blend_file_path = bpy.data.filepath
        directory = os.path.dirname(bpy.path.abspath(scene.custom_props.outputpath))

        lowref = scene.custom_props.low_ref
        highref = scene.custom_props.high_ref
        fbxanimbake = scene.custom_props.bakeanim
        fbxapplymods = scene.custom_props.applymods
        fbxsmooth = scene.custom_props.smoothing
        objanim = scene.custom_props.anim
        objsmooth = scene.custom_props.smoothingo

        mats = scene.custom_props.materials
        tri = scene.custom_props.triangulate
        fname = scene.custom_props.filename

        try:
            iter(sObjs)
            for o in sObjs:
                if lowref in o.name:
                    lows.append(o)
                elif highref in o.name:
                    highs.append(o)
        except TypeError:
            print("Not an iterable.")

        #check that directory isn't empty, otherwise set it to blend_file_path
        if directory is "":
            directory = os.path.dirname(bpy.path.abspath(blend_file_path))

        if scene.custom_props.fileperobject:
            if lows:
                for l in lows:
                    lname = l.name
                    bpy.data.objects[lname].select_set(True)
                    if scene.custom_props.export_filetype is '0':
                        target_file = os.path.join(directory, lname + ".fbx")
                        bpy.ops.export_scene.fbx(filepath = target_file, check_existing = True, use_selection = True, path_mode = 'AUTO', 
                            bake_anim = fbxanimbake, use_mesh_modifiers = fbxapplymods, mesh_smooth_type = fbxsmooth)
                    elif scene.custom_props.export_filetype is '1':
                        target_file = os.path.join(directory, lname + ".obj")
                        bpy.ops.export_scene.fbx(filepath = target_file, check_existing = True, use_selection = True, path_mode = 'AUTO', 
                            bake_anim = fbxanimbake, use_mesh_modifiers = fbxapplymods, mesh_smooth_type = fbxsmooth)
                            
            if highs:
                for h in highs:
                    hname = h.name
                    bpy.data.objects[hname].select_set(True)
                    if scene.custom_props.export_filetype is '0':
                        target_file = os.path.join(directory, hname + ".fbx")
                        bpy.ops.export_scene.fbx(filepath = target_file, check_existing = True, use_selection = True, path_mode = 'AUTO', 
                            bake_anim = fbxanimbake, use_mesh_modifiers = fbxapplymods, mesh_smooth_type = fbxsmooth)
                    elif scene.custom_props.export_filetype is '1':
                        target_file = os.path.join(directory, hname + ".obj")
                        bpy.ops.export_scene.fbx(filepath = target_file, check_existing = True, use_selection = True, path_mode = 'AUTO', 
                            bake_anim = fbxanimbake, use_mesh_modifiers = fbxapplymods, mesh_smooth_type = fbxsmooth)
        else:
            #Export low poly meshes
            if lows:
                bpy.ops.object.select_all(action = 'DESELECT')
                for l in lows:
                    bpy.data.objects[l.name].select_set(True)
                if scene.custom_props.export_filetype is '0':
                    #export as FBX, change directory to have a name and _low.fbx appended
                    target_file = os.path.join(directory, fname + lowref + ".fbx")
                    bpy.ops.export_scene.fbx(filepath = target_file, check_existing = True, use_selection = True, path_mode = 'AUTO', 
                    bake_anim = fbxanimbake, use_mesh_modifiers = fbxapplymods, mesh_smooth_type = fbxsmooth)
                elif scene.custom_props.export_filetype is '1':
                    #export as OBJ, ditto
                    target_file = os.path.join(directory, fname + lowref + ".obj")
                    bpy.ops.export_scene.obj(filepath = target_file, check_existing = True, use_selection = True, path_mode = 'AUTO', 
                    use_animation = objanim, use_smooth_groups = objsmooth, use_materials = mats, use_triangles = tri)

            #export high poly meshes
            if highs:
                bpy.ops.object.select_all(action = 'DESELECT')
                for h in highs:
                    bpy.data.objects[h.name].select_set(True)
                if scene.custom_props.export_filetype is '0':
                    #export as FBX
                    target_file = os.path.join(directory, fname + highref + ".fbx")
                    bpy.ops.export_scene.fbx(filepath = target_file, check_existing = True, use_selection = True, path_mode = 'AUTO', 
                    bake_anim = False, use_mesh_modifiers = fbxapplymods, mesh_smooth_type= fbxsmooth)
                elif scene.custom_props.export_filetype is '1':
                    #export as OBJ
                    target_file = os.path.join(directory, fname + highref + ".obj")
                    bpy.ops.export_scene.obj(filepath = target_file, check_existing = True, use_selection = True, path_mode = 'AUTO',
                    use_animation = False, use_smooth_groups = objsmooth, use_materials = False, use_triangles = False)

        return {'FINISHED'}