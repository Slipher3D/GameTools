import bpy

class Gtools_PT_Panel(bpy.types.Panel):
    bl_idname = "Gtools_PT_Panel"
    bl_label = "Game Tools"
    bl_category = "Game Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        props = context.scene.custom_props

        #MOR elements
        box = layout.box()
        row = box.row()
        row = box.label(text = "Multi-Object Renamer")
        #Name property
        row = box.row(align = True)
        row = box.prop(props, 'name')
        #Prefix property
        row = box.row(align = True)
        row = box.prop(props, 'prefix')
        #Suffix property
        row = box.row(align = True)
        row = box.prop(props, 'suffix')
        #UseNum property
        row = box.row(align = True)
        row = box.prop(props, 'usenums')
        if props.usenums is True:
            #StartNum property
            row = box.row(align = True)
            row = box.prop(props, 'startnum')
            #StepNum property
            row = box.row(align = True)
            row = box.prop(props, 'step')
        #MOR Operator Button
        row = box.row()
        row = box.operator('object.morenamer', text = "Rename")
        
        #Lightingcrest elements
        box = layout.box()
        row = box.row(align = True)
        row = box.label(text = "Export")
        #Outputpath property
        row = box.row(align = True)
        row = box.prop(props, 'fileperobject')
        #export filename property
        row = box.row(align = True)
        row = box.prop(props, 'filename')
        #low reference property
        row = box.row(align = True)
        row.prop(props, 'low_ref')
        #high reference property
        row.prop(props, 'high_ref')
        #output path property
        row = box.row(align = True)
        row = box.prop(props, 'outputpath')
        #export filetype property
        row = box.row(align = True)
        row = box.prop(props, 'export_filetype')

        if props.export_filetype is '0':
            #FBX Options label
            row = box.row(align = True)
            box.label(text = "FBX Options")
            #bake bool, applymods bool
            row = box.row(align = True)
            row.prop(props, 'bakeanim')
            row.prop(props, 'applymods')
            #smoothing list
            row = box.row(align = True)
            row = row.prop(props, 'smoothing')
        elif props.export_filetype is '1':
            #OBJ Options label
            row = box.row(align = True)
            box.label(text = "OBJ Options")
            #anim, smooth bool
            row = box.row(align = True)
            row.prop(props, 'anim')
            row.prop(props, 'smoothingo')
            #materials, triangulate bool
            row = box.row(align = True)
            row.prop(props, 'materials')
            row.prop(props, 'triangulate')
        #lcexporter operator
        row = box.row(align = True)
        row = box.operator('object.lcexporter', text = "Export")