import bpy
from mathutils import Vector


class ResetStretch(bpy.types.Operator):
    bl_idname = "armature_snippets.reset_stretch"
    bl_label = "Reset stretch"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    
    @classmethod
    def poll(cls, context):
        if context.active_object:
            return context.active_object.mode == "POSE"
    
    def execute(self, context):
        ob = context.active_object
        bones = context.selected_pose_bones
        last_active_bone = ob.data.bones.active
        for bone in bones:
            c_type_list = [c.type for c in bone.constraints]
            for index, type in enumerate(c_type_list):
                if type == "STRETCH_TO":
                    constraint = bone.constraints[index]
                    c = context.copy()
                    c["constraint"] = constraint
                    ob.data.bones.active = bone.bone
                    bpy.ops.constraint.stretchto_reset(c, constraint = constraint.name, owner = "BONE")
        ob.data.bones.active = last_active_bone
        return {"FINISHED"}


class ResetStretch(bpy.types.Operator):
    bl_idname = "armature_snippets.reset_limitdistance"
    bl_label = "Reset limit distance"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    
    @classmethod
    def poll(cls, context):
        if context.active_object:
            return context.active_object.mode == "POSE"
    
    def execute(self, context):
        ob = context.active_object
        bones = context.selected_pose_bones
        last_active_bone = ob.data.bones.active
        for bone in bones:
            c_type_list = [c.type for c in bone.constraints]
            for index, type in enumerate(c_type_list):
                if type == "LIMIT_DISTANCE":
                    constraint = bone.constraints[index]
                    c = context.copy()
                    c["constraint"] = constraint
                    ob.data.bones.active = bone.bone
                    bpy.ops.constraint.limitdistance_reset(c, constraint = constraint.name, owner = "BONE")
        ob.data.bones.active = last_active_bone
        return {"FINISHED"}