from pyroll import RollPass

from . import specs
from . import impls

RollPass.plugin_manager.add_hookspecs(specs)
RollPass.plugin_manager.register(impls)
