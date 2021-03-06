bl_info = {
    "sender_name": "RenderStack Node ",
    "author"     : "Atticus",
    "version"    : (1, 0, 7),
    "blender"    : (2, 92, 0),
    "location"   : "Node Editor > RenderStackNode Editor",
    "description": "Node based render queue workflow",
    'warning'     : "Use Cuda to render may cause python state error! ",
    # "doc_url"    : "",
    "category"   : "Render",
}

import importlib
import sys
import bpy
from .nodes import *
from .rsn_helper import *

__dict__ = {}
__dict__['preferences'] = f"{__name__}.preferences"
__dict__["node_tree"] = f"{__name__}.node_tree"
__dict__['utility'] = f'{__name__}.utility'

for k, v in a.items():
    for module_name in v:
        __dict__[module_name] = f"{__name__}.nodes.{k}.{module_name}"

for k, v in b.items():
    for module_name in v:
        __dict__[module_name] = f"{__name__}.rsn_helper.{k}.{module_name}"

for name in __dict__.values():
    if name in sys.modules:
        importlib.reload(sys.modules[name])
    else:
        globals()[name] = importlib.import_module(name)
        setattr(globals()[name], 'modules', __dict__)


def register():
    for name in __dict__.values():
        if name in sys.modules and hasattr(sys.modules[name], 'register'):
            sys.modules[name].register()


def unregister():
    for name in __dict__.values():
        if name in sys.modules and hasattr(sys.modules[name], 'unregister'):
            sys.modules[name].unregister()


if __name__ == '__main__':
    register()
