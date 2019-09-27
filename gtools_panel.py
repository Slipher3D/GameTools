import bpy

class Gtools_PT_Panel(bpy.types.Panel):
    bl_idname = "Gtools_PT_Panel"
    bl_label = "Game Tools"
    bl_category = "Game Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('object.bsd', text = "Bevel SubSurf")
        row2 = layout.row()
        row2.operator('object.morenamer', text = "Multi-Object Renamer")