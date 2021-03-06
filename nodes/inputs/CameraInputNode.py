import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


def poll_camera(self, object):
    return object.type == 'CAMERA'


def update_node(self, context):
    self.update()


class RSNodeCamInputNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeCamInputNode'
    bl_label = 'Camera'

    camera: PointerProperty(name="Camera", type=bpy.types.Object, poll=poll_camera, update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketCamera', "Camera")
        self.width = 150

    def draw_buttons(self, context, layout):
        layout.prop(self, 'camera', text="")


def register():
    bpy.utils.register_class(RSNodeCamInputNode)


def unregister():
    bpy.utils.unregister_class(RSNodeCamInputNode)
