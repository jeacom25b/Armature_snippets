import importlib
import bpy


bl_info = {
    "name": "Armature snippets",
    "description": "",
    "author": "Jean Da Costa Machado",
    "version": (0, 0, 1),
    "blender": (2, 78, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Rigging"}

from . import loadsave
from . import preferences
from . import interface
from . import bindpose_utils


if "bpy" in locals():
    importlib.reload(loadsave)
    importlib.reload(preferences)
    importlib.reload(interface)
    importlib.reload(bindpose_utils)


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.armature_snippet_index = bpy.props.IntProperty()
    bpy.types.Scene.armature_snippet_list = bpy.props.CollectionProperty(type = interface.ArmatureSnippetsPGroup)


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.armature_snippet_index
    del bpy.types.Scene.armature_snippet_list


if __name__ == "__main__":
    register()
