from pyroll.core import RollPass


@RollPass.hookspec
def roll_gap_ratio(roll_pass):
    """Calculate cross section ratio used in Hensel-Poluchin master curves."""


@RollPass.hookspec
def rolling_efficiency(roll_pass):
    """Calculate rolling efficiency according to Hensel-Poluchin master curve."""


@RollPass.hookspec
def deformation_resistance(roll_pass):
    """Calculate deformation resistance according to Hensel-Poluchin master curve."""


@RollPass.hookspec
def lever_arm_coefficient(roll_pass):
    """Calculate lever coefficient according to Hensel-Poluchin master curve."""
