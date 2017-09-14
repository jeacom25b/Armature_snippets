import bpy
from mathutils import Vector
import math


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


class ResetLimdist(bpy.types.Operator):
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


# context is the bpy.context,
# p_bone is the pose bone with the constraint
# ik is the Inverse kinimatics constraint on the p_bone
# angle is the angle to try and score
def ik_test(context, p_bone, ik, angle):
    # mute constraint for getting original vectors of the bone
    ik.mute = True
    # then update the scene
    context.scene.frame_set(context.scene.frame_current)
    # get some vecotrs
    v1 = p_bone.vector.copy()
    x1 = p_bone.x_axis.copy()
    z1 = p_bone.z_axis.copy()
    
    # unmute the constraint
    ik.mute = False
    # set the pole_angle for the test
    ik.pole_angle = angle
    # update the scene again
    context.scene.frame_set(context.scene.frame_current)
    # get the new vectors
    v2 = p_bone.vector.copy()
    x2 = p_bone.x_axis.copy()
    z2 = p_bone.z_axis.copy()
    
    # lets see the diferences..
    v_point = (v1 - v2).magnitude
    x_point = (x1 - x2).magnitude
    z_point = (z1 - z2).magnitude
    # lets get the total score
    total = v_point + x_point + z_point
    # with better score total sould be smaller,
    # but it returns zero at multiple angles
    # this only can happen if the scene does't update.
    print(angle, total)
    return (angle, total)


# a siple leerp functinon
def lerp(x, y, c):
    a = x * (1 - c)
    b = y * c
    return a + b


class FindIkPole(bpy.types.Operator):
    bl_idname = "armature_snippets.find_ik_pole_angle"
    bl_label = "Find IK pole Angle"
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
                if type == "IK":
                    ik = bone.constraints[index]
                    if not ik.mute:
                        
                        n1 = -180
                        n2 = 180
                        
                        tests = []
                        for i in range(11):
                            c = i / 10
                            angle = lerp(n1, n2, c)
                            tests.append(ik_test(context, bone, ik, angle))
                        
                        print(tests)
        
        ob.data.bones.active = last_active_bone
        return {"FINISHED"}
