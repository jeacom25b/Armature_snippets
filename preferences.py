import bpy
import os

class Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__.split(".")[0]
    
    save_path = bpy.props.StringProperty("Library Path",
                                         subtype = "FILE_PATH",
                                         default = os.path.join(bpy.utils.resource_path("USER"),
                                                                "config",
                                                                "armature_snippets")
                                         )
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "save_path", "Snippets folder")
