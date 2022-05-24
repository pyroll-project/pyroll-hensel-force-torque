from pyroll.core import RollPass
from pyroll.ui import Reporter
from pyroll.utils import for_units


@Reporter.hookimpl
@for_units(RollPass)
def unit_properties(unit: RollPass):
    return dict(
        roll_gap_ratio=f"{unit.roll_gap_ratio:.2f}",
        deformation_resistance=f"{unit.deformation_resistance:.4g}",
        lever_arm_coefficient=f"{unit.lever_arm_coefficient:.2f}",
        rolling_efficiency=f"{unit.rolling_efficiency:.2f}"
    )
