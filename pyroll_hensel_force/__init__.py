from pyroll import RollPass
from pyroll import Exporter
from pyroll import Reporter

from . import specs
from . import impls

RollPass.plugin_manager.add_hookspecs(specs)
RollPass.plugin_manager.register(impls)

from . import report

Reporter.plugin_manager.register(report)

from . import export

Exporter.plugin_manager.register(export)
