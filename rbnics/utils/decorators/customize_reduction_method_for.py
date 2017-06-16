# Copyright (C) 2015-2017 by the RBniCS authors
#
# This file is part of RBniCS.
#
# RBniCS is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RBniCS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RBniCS. If not, see <http://www.gnu.org/licenses/>.
#

import inspect

def CustomizeReductionMethodFor(Problem):
    assert inspect.isabstract(Problem), "It is suggested to use this customizer for abstract classes (e.g., before specifying theta terms and operators, or decorating with EIM or SCM), because otherwise the customization would not be preserved with a call to exact_problem."
    def CustomizeReductionMethodFor_Decorator(customizer):
        CustomizeReductionMethodFor._all_reduction_method_customizers[Problem] = customizer
        return customizer
    return CustomizeReductionMethodFor_Decorator

CustomizeReductionMethodFor._all_reduction_method_customizers = dict() # dicts from Problem to decorator
