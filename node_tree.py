import bpy
import nodeitems_utils
from bpy.props import *
from RenderStackNode.utility import trace_back_node


class RenderStackNodeTree(bpy.types.NodeTree):
    '''RenderStackNodeTree Node Tree'''
    bl_idname = 'RenderStackNodeTree'
    bl_label = 'RenderStackNode Editor'
    bl_icon = 'CAMERA_DATA'


class RenderStackNode(bpy.types.Node):
    bl_label = "RenderStack Node"

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'RenderStackNodeTree'

    def copy(self, node):
        print("RSN Copied node", node.name)

    def free(self):
        print("RSN removed node", self.name)

    def update(self):
        try:
            if self.outputs[0].is_linked:
                task_node = trace_back_node(self.name, node_type='RSNodeTaskNode')
                viewer = trace_back_node(self.name, node_type='RSNodeViewerNode')

                if task_node and viewer:
                    if not True in {task_node.mute, viewer.mute}:
                        try:
                            pref = bpy.context.preferences.addons.get('RenderStackNode').preferences
                            bpy.ops.rsn.update_parms(task_name=task_node.name,
                                                     viewer_handler=bpy.context.window_manager.rsn_viewer_node,
                                                     update_scripts=pref.node_viewer.update_scripts,
                                                     use_render_mode=False)
                        except Exception as e:
                            print(e)
        except (IndexError):
            pass


class RenderStackNodeGroup(bpy.types.NodeCustomGroup):
    bl_label = 'RenderStack Node Group'

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'RenderStackNodeTree'


#
#  Sockets
#


class RSNodeSocketCamera(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketCamera'
    bl_label = 'RSNodeSocketCamera'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0, 0.8, 1.0, 1.0)


class RSNodeSocketTaskSettings(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketTaskSettings'
    bl_label = 'RSNodeSocketTaskSettings'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.5, 0.5, 0.5, 1.0)


class RSNodeSocketRenderSettings(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketRenderSettings'
    bl_label = 'RSNodeSocketRenderSettings'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0, 1, 0, 1.0)


class RSNodeSocketOutputSettings(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketOutputSettings'
    bl_label = 'RSNod   eSocketOutputSettings'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0, 0, 1, 1.0)


class RSNodeSocketRenderList(bpy.types.NodeSocket):
    bl_idname = 'RSNodeSocketRenderList'
    bl_label = 'RSNodeSocketRenderList'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.5, 0.3, 0.7, 1.0)


#
#  Category
#

class RSNCategory(nodeitems_utils.NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'RenderStackNodeTree'


node_categorys = [

    RSNCategory("INPUT", "Input", items=[
        nodeitems_utils.NodeItem("RSNodeCamInputNode"),
        nodeitems_utils.NodeItem("RSNodeWorldInputNode"),
        nodeitems_utils.NodeItem('RSNodeViewLayerInputNode'),
        nodeitems_utils.NodeItem('RSNodeObjectMaterialNode'),
        nodeitems_utils.NodeItem('RSNodeObjectPSRNode'),
        # nodeitems_utils.NodeItem('RSNodeObjectDataNode'),
        nodeitems_utils.NodeItem('RSNodeColorManagementNode'),
    ]),

    RSNCategory("TASK", "Task", items=[
        nodeitems_utils.NodeItem("RSNodeTaskNode"),
        nodeitems_utils.NodeItem("RSNodeTaskListNode"),
        nodeitems_utils.NodeItem("RSNodeRenderListNode"),
        nodeitems_utils.NodeItem("RSNodeProcessorNode"),
        nodeitems_utils.NodeItem("RSNodeViewerNode"),

    ]),

    RSNCategory("SCRIPTS", "Scripts", items=[
        nodeitems_utils.NodeItem("RSNodeScriptsNode"),
        nodeitems_utils.NodeItem("RSNodeSmtpEmailNode"),
        nodeitems_utils.NodeItem("RSNodeLightStudioNode"),
        # nodeitems_utils.NodeItem("RSNodeServerNode"),
        # nodeitems_utils.NodeItem("RSNodeClientNode"),
    ]),

    RSNCategory("OUTPUT_SETTINGS", "Output Settings", items=[
        nodeitems_utils.NodeItem("RSNodeResolutionInputNode"),
        nodeitems_utils.NodeItem("RSNodeFrameRangeInputNode"),
        nodeitems_utils.NodeItem("RSNodeImageFormatInputNode"),
        nodeitems_utils.NodeItem("RSNodeFilePathInputNode"),
        nodeitems_utils.NodeItem("RSNodeActiveRenderSlotNode"),
        nodeitems_utils.NodeItem("RSNodeViewLayerPassesNode"),
    ]),

    RSNCategory("RENDER_SETTINGS", "Render Settings", items=[
        nodeitems_utils.NodeItem("RSNodeWorkBenchRenderSettingsNode"),
        nodeitems_utils.NodeItem("RSNodeEeveeRenderSettingsNode"),
        nodeitems_utils.NodeItem("RSNodeCyclesRenderSettingsNode"),
        nodeitems_utils.NodeItem("RSNodeCyclesLightPathNode"),
        nodeitems_utils.NodeItem("RSNodeLuxcoreRenderSettingsNode"),

    ]),

    RSNCategory("LAYOUT", "Layout", items=[
        nodeitems_utils.NodeItem("RSNodeSettingsMergeNode", label="Merge Settings", settings={
            "node_type": repr("RENDER_SETTINGS"),
        }),

    ]),
]

classes = [
    RenderStackNodeTree,
    RenderStackNode,
    RenderStackNodeGroup,
    # Socker
    RSNodeSocketCamera,
    RSNodeSocketRenderSettings,
    RSNodeSocketOutputSettings,
    RSNodeSocketTaskSettings,
    RSNodeSocketRenderList,
]


def register():
    try:
        nodeitems_utils.unregister_node_categories("RSNCategory")
    except:
        pass

    for cls in classes:
        bpy.utils.register_class(cls)

    nodeitems_utils.register_node_categories("RSNCategory", node_categorys)


def unregister():
    nodeitems_utils.unregister_node_categories("RSNCategory")

    for cls in classes:
        bpy.utils.unregister_class(cls)
