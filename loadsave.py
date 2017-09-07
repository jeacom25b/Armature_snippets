import bpy
import os


def add_extension(name):
    if not name[-6:].upper() == ".BLEND":
        return ".".join([name, "blend"])


class LoadArmature(bpy.types.Operator):
    bl_idname = "armature_snippets.load_armature"
    bl_label = "Load Armature"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    
    snippet_name = bpy.props.StringProperty(name = "Name")
    join = bpy.props.BoolProperty(name = "Join to active", default = True)
    
    def execute(self, context):
        path = context.user_preferences.addons[__name__.split(".")[0]].preferences.save_path
        file_name = add_extension(self.snippet_name)
        file_path = os.path.join(path, file_name)
        
        data_name = ""
        object_mame = ""
        object_active = context.active_object
        
        if os.path.isfile(os.path.join(path, file_name)):
            with bpy.data.libraries.load(file_path) as (data_from, data_to):
                data_to.armatures = [data_from.armatures[0]]
                data_to.objects = [data_from.objects[0]]
                data_name = data_from.armatures[0]
                object_mame = data_from.objects[0]
        
        if not data_name is "" and not object_mame is "":
            armature = bpy.data.armatures[data_name]
            armature.name = self.snippet_name
            ob = bpy.data.objects[object_mame]
            ob.name = self.snippet_name
            ob.location = context.scene.cursor_location
            armature_object = context.scene.objects.link(ob)
            
            if self.join:
                if context.active_object:
                    if object_active.type == "ARMATURE":
                        last_mode = object_active.mode
                        bpy.ops.object.mode_set(mode = "OBJECT")
                        bpy.ops.object.select_all(action = "DESELECT")
                        object_active.select = True
                        context.scene.objects.active = object_active
                        armature_object.select = True
                        bpy.ops.object.join()
                        bpy.ops.object.mode_set(mode = last_mode)
        
        else:
            self.report({"ERROR"}, "Failed")
            return {"CANCELLED"}
        
        bpy.ops.armature_snippets.list_files()
        
        return {"FINISHED"}


class SaveArmature(bpy.types.Operator):
    bl_idname = "armature_snippets.save_armature"
    bl_label = "Save Armature"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    
    snippet_name = bpy.props.StringProperty()
    compress = bpy.props.BoolProperty(default = True)
    
    @classmethod
    def poll(cls, context):
        if context.active_object:
            return context.active_object.type == "ARMATURE"
    
    def execute(self, context):
        ob = {context.active_object}
        path = context.user_preferences.addons[__name__.split(".")[0]].preferences.save_path
        file_name = add_extension(self.snippet_name)
        blend_path = os.path.join(path, file_name)
        
        if not os.path.exists(blend_path):
            try:
                os.makedirs(path)
            except:
                pass
        if not os.path.isfile(blend_path):
            bpy.data.libraries.write(blend_path, ob, compress = self.compress, fake_user = True)
        else:
            self.report({"WARNING"}, "Name already exists, pick another")
        
        bpy.ops.armature_snippets.list_files()
        
        return {"FINISHED"}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "snippet_name", "Name")
        layout.prop(self, "compress", "Compress")
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class DeleteArmature(bpy.types.Operator):
    bl_idname = "armature_snippets.delete_armature"
    bl_label = "Delete Armature"
    bl_description = ""
    bl_options = {"REGISTER"}
    
    snippet_name = bpy.props.StringProperty()
    confirm_delete = bpy.props.BoolProperty(default = False)
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        if not self.confirm_delete:
            self.report({"INFO"}, "Need confirmation, operation Cancelled")
            return {"CANCELLED"}
        
        ob = {context.active_object}
        path = context.user_preferences.addons[__name__.split(".")[0]].preferences.save_path
        file_name = add_extension(self.snippet_name)
        blend_path = os.path.join(path, file_name)
        
        if not os.path.exists(blend_path):
            try:
                os.makedirs(path)
            except:
                pass
        if os.path.isfile(blend_path):
            os.remove(blend_path)
            self.report({"INFO"}, "File (%s) deleted" % (file_name))
        else:
            self.report({"ERROR"}, "File (%s) not found or inaceesible" % (blend_path))
        
        bpy.ops.armature_snippets.list_files()
        
        return {"FINISHED"}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "snippet_name", "Name")
        row = layout.row()
        row.label("Are you sure you want to delete?")
        row.prop(self, "confirm_delete", "yes")
    
    def invoke(self, context, event):
        self.confirm_delete = False
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class ListFiles(bpy.types.Operator):
    bl_idname = "armature_snippets.list_files"
    bl_label = "Update list"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        path = context.user_preferences.addons[__name__.split(".")[0]].preferences.save_path
        items = os.listdir(path)
        files = []
        for file in items:
            possible_file = os.path.join(path, file)
            if os.path.isfile(possible_file):
                if file[-6:].upper != ".blend":
                    files.append(file[:-6])
        context.scene.armature_snippet_list.clear()
        for f in files:
            item = context.scene.armature_snippet_list.add()
            item.name = f
        return {"FINISHED"}
