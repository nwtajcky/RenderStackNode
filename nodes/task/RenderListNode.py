import json
import bpy

from bpy.props import *
from RenderStackNode.utility import *
from RenderStackNode.node_tree import RenderStackNode
from .ProcessorNode import RSNodeProcessorNode


class RSNode_OT_GetInfo(bpy.types.Operator):
    '''left click: get node name
shift:get overwrite details '''
    bl_idname = 'rsn.get_info'
    bl_label = 'get info'

    def invoke(self, context, event):
        rsn_tree = RSN_NodeTree()
        rsn_tree.set_context_tree_as_wm_tree()

        nt = rsn_tree.get_wm_node_tree()
        rsn_task = RSN_Task(node_tree=self.nt,
                            root_node_name=self.render_list_node_name)

        if event.shift:
            for k in nt.node_list_dict.keys():
                print(json.dumps(nt.get_task_data(k), indent=4, ensure_ascii=False))
        else:
            print(json.dumps(nt.node_list_dict, indent=4, ensure_ascii=False))

        return {"FINISHED"}


class RSNodeRenderListNode(RenderStackNode):
    '''Render List Node'''
    bl_idname = 'RSNodeRenderListNode'
    bl_label = 'Render List'

    show_process: BoolProperty(name='Show Processor Node')

    def init(self, context):
        self.inputs.new('RSNodeSocketRenderList', "Task")

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        # edit Inputs
        layout.scale_y = 1.25
        # layout.operator("rsn.get_info", text=f'Print Info (Console)')
        box = layout.box()
        box.scale_y = 1.5
        box.operator("rsn.render_button", text=f'Render Inputs').render_list_node_name = self.name

        # layout.prop(self,"show_process")




def register():
    bpy.utils.register_class(RSNodeRenderListNode)
    bpy.utils.register_class(RSNode_OT_GetInfo)


def unregister():
    bpy.utils.unregister_class(RSNodeRenderListNode)
    bpy.utils.unregister_class(RSNode_OT_GetInfo)
