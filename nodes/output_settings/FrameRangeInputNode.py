import bpy
from bpy.props import *
from RenderStackNode.node_tree import RenderStackNode


class RSNodeFrameRangeInputNode(RenderStackNode):
    bl_idname = "RSNodeFrameRangeInputNode"
    bl_label = "Frame Range"

    frame_start: IntProperty(name="Frame Start", default=1, min=0)
    frame_end: IntProperty(name="Frame End", default=1, min=0)
    frame_step: IntProperty(name="Frame Step", default=1, min=1)

    def init(self, context):
        self.outputs.new('RSNodeSocketOutputSettings', "Output Settings")

    def draw_buttons(self, context, layout):
        col = layout.column(align=1)
        col.prop(self, 'frame_start')
        col.prop(self, 'frame_end')
        col.prop(self, 'frame_step')


def register():
    bpy.utils.register_class(RSNodeFrameRangeInputNode)


def unregister():
    bpy.utils.unregister_class(RSNodeFrameRangeInputNode)
