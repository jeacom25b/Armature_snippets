import bpy


class ArmatureSnippetsUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index=0, flt_flag=0):
        layout.label(item.name, icon = "FILE_BLEND")


class ArmatureSnippetsPGroup(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty()


class ArmatureSnippetsPannel(bpy.types.Panel):
    bl_idname = "armature_snippets.panel"
    bl_label = "Armature snippets"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    
    @classmethod
    def pool(cls, context):
        if context.actve_object:
            return context.active_object.mode != "SCULPT"
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.label("Saved armatures")
        row = layout.row()
        row.template_list("ArmatureSnippetsUIList", "", scn, "armature_snippet_list", scn, "armature_snippet_index")
        row.operator("armature_snippets.list_files", "", icon = "FILE_REFRESH")

        layout.operator("armature_snippets.save_armature")

        snippets_list = snippet_name = context.scene.armature_snippet_list
        if len(snippets_list) > 0:
            snippet_name = snippets_list[context.scene.armature_snippet_index].name
            layout.operator("armature_snippets.load_armature").snippet_name = snippet_name
            layout.operator("armature_snippets.delete_armature").snippet_name = snippet_name
