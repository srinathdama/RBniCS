# Copyright (C) 2015-2018 by the RBniCS authors
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

from numbers import Number
from numpy import isclose
from rbnics.utils.decorators import PreserveClassName, RequiredBaseDecorators
from rbnics.utils.test import PatchInstanceMethod

@RequiredBaseDecorators(None)
def TimeDependentReductionMethod(DifferentialProblemReductionMethod_DerivedClass):
    
    @PreserveClassName
    class TimeDependentReductionMethod_Class(DifferentialProblemReductionMethod_DerivedClass):
        
        # Default initialization of members
        def __init__(self, truth_problem, **kwargs):
            # Call to parent
            DifferentialProblemReductionMethod_DerivedClass.__init__(self, truth_problem, **kwargs)
            
            # Indices for undersampling snapshots, e.g. after a transient
            self.reduction_first_index = None # keep temporal evolution from the beginning by default
            self.reduction_delta_index = None # keep every time step by default
            self.reduction_last_index = None # keep temporal evolution until the end by default
            
        # Set reduction initial time
        def set_reduction_initial_time(self, t0):
            assert isinstance(t0, Number)
            assert t0 >= self.truth_problem.t0
            self.reduction_first_index = int(t0/self.truth_problem.dt)
                    
        # Set reduction time step size
        def set_reduction_time_step_size(self, dt):
            assert isinstance(dt, Number)
            assert dt >= self.truth_problem.dt
            self.reduction_delta_index = int(dt/self.truth_problem.dt)
            assert isclose(self.reduction_delta_index*self.truth_problem.dt, dt), "Reduction time step size should be a multiple of discretization time step size"
            
        # Set reduction final time
        def set_reduction_final_time(self, T):
            assert isinstance(T, Number)
            assert T <= self.truth_problem.T
            self.reduction_last_index = int(T/self.truth_problem.dt)
            
        def postprocess_snapshot(self, snapshot_over_time, snapshot_index):
            postprocessed_snapshot = list()
            for (k, snapshot_k) in enumerate(snapshot_over_time):
                self.reduced_problem.set_time(k*self.reduced_problem.dt)
                postprocessed_snapshot_k = DifferentialProblemReductionMethod_DerivedClass.postprocess_snapshot(self, snapshot_k, snapshot_index)
                postprocessed_snapshot.append(postprocessed_snapshot_k)
            return postprocessed_snapshot
        
        # Initialize data structures required for the speedup analysis phase
        def _init_speedup_analysis(self, **kwargs):
            DifferentialProblemReductionMethod_DerivedClass._init_speedup_analysis(self, **kwargs)
            # Parent method had already patched import/export, but with the wrong signature
            self.disable_import_solution.unpatch()
            self.disable_export_solution.unpatch()
            del self.disable_import_solution
            del self.disable_export_solution
            
            # Make sure to clean up problem and reduced problem solution cache to ensure that
            # solution and reduced solution are actually computed
            self.truth_problem._solution_dot_cache.clear()
            self.reduced_problem._solution_dot_cache.clear()
            self.truth_problem._solution_over_time_cache.clear()
            self.reduced_problem._solution_over_time_cache.clear()
            self.truth_problem._solution_dot_over_time_cache.clear()
            self.reduced_problem._solution_dot_over_time_cache.clear()
            self.truth_problem._output_over_time_cache.clear()
            self.reduced_problem._output_over_time_cache.clear()
            # ... and also disable the capability of importing/exporting truth solutions
            self.disable_import_solution = PatchInstanceMethod(
                self.truth_problem,
                "import_solution",
                lambda self_, folder=None, filename=None, solution_over_time=None, component=None, suffix=None: False
            )
            self.disable_export_solution = PatchInstanceMethod(
                self.truth_problem,
                "export_solution",
                lambda self_, folder=None, filename=None, solution_over_time=None, component=None, suffix=None: None
            )
            self.disable_import_solution.patch()
            self.disable_export_solution.patch()
        
    # return value (a class) for the decorator
    return TimeDependentReductionMethod_Class
