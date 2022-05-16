import numpy as np
from pyroll.core import RollPass


@RollPass.hookimpl
def roll_gap_ratio(roll_pass: RollPass):
    mean_cross_section = (roll_pass.in_profile.cross_section.area + 2 * roll_pass.out_profile.cross_section.area) / 3
    return roll_pass.roll.contact_area / mean_cross_section


@RollPass.hookimpl
def rolling_efficiency(roll_pass: RollPass):
    inverse_efficiency = (0.9901 + 0.106 * roll_pass.roll_gap_ratio + 0.0283 * roll_pass.roll_gap_ratio ** 2
                          + 1.5718 * np.exp(-2.4609 * roll_pass.roll_gap_ratio)
                          + 0.3117 * np.exp(-15.625 * roll_pass.roll_gap_ratio ** 2))
    return inverse_efficiency ** -1


@RollPass.hookimpl
def deformation_resistance(roll_pass: RollPass):
    mean_flow_stress = (roll_pass.in_profile.flow_stress + 2 * roll_pass.out_profile.flow_stress) / 3
    return mean_flow_stress / roll_pass.rolling_efficiency


@RollPass.hookimpl
def lever_arm_coefficient(roll_pass: RollPass):
    mean_temperature = (roll_pass.in_profile.temperature + roll_pass.out_profile.temperature) / 2
    return ((np.exp(-0.6 * roll_pass.roll_gap_ratio) + 0.076 * roll_pass.roll_gap_ratio)
            * roll_pass.velocity ** 0.005 * np.exp(
                -0.0003 * (mean_temperature - 273.15 - 900)))


@RollPass.hookimpl
def roll_force(roll_pass: RollPass):
    return roll_pass.deformation_resistance * roll_pass.roll.contact_area


@RollPass.Roll.hookimpl
def roll_torque(roll_pass: RollPass, roll: RollPass.Roll):
    return roll_pass.roll_force * roll.contact_length * roll_pass.lever_arm_coefficient
