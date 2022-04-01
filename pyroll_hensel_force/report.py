from pyroll import RollPass
from pyroll.ui.report import Report
from pyroll.utils import applies_to_unit_types


@Report.hookimpl
@applies_to_unit_types(RollPass)
def unit_properties(unit: RollPass):
    return dict(
        cross_section_ratio=f"{unit.cross_section_ratio:.2f}",
        deformation_resistance=f"{unit.deformation_resistance:.4g}",
        lever_coefficient=f"{unit.lever_coefficient:.2f}",
        rolling_efficiency=f"{unit.rolling_efficiency:.2f}"
    )
