#  SPDX-FileCopyrightText: 2022 easyCrystallography contributors  <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022 Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>
#

__author__ = 'github.com/wardsimon'
__version__ = '0.1.0'

from easyCrystallography.Symmetry.SymOp import SymmOp


class Twin:
    def __init__(self, origin=(0, 0, 0), theta: float = 0.0, phi: float = 0.0):
        self.theta = theta
        self.phi = phi
        self.origin = list(origin)
        self.axis1 = [1, 0, 0]
        self.axis2 = [0, 0, 1]

    @property
    def operation(self):
        return SymmOp.from_origin_axis_angle(self.origin, self.axis1, self.phi) * \
                SymmOp.from_origin_axis_angle(self.origin, self.axis2, self.theta)
