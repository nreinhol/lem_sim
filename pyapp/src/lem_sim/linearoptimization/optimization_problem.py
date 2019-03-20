from scipy.optimize import linprog


class OptimizationProblem():

    def __init__(self, target_coefs, constraint_coefs, constraint_bounds):
        self._target_coefs = target_coefs
        self._constraint_coefs = constraint_coefs
        self._constraint_bounds = constraint_bounds

    @property
    def target_coefs(self):
        return self._target_coefs

    @target_coefs.setter
    def target_coefs(self, values):
        self._target_coefs = values

    @property
    def constraint_coefs(self):
        return self._constraint_coefs

    @constraint_coefs.setter
    def constraint_coefs(self, values):
        self._constraint_coefs = values

    @property
    def constraint_bounds(self):
        return self._constraint_bounds

    @constraint_bounds.setter
    def constraint_bounds(self, values):
        self._constraint_bounds = values

    def solve(self):
        result = linprog(self._target_coefs, A_ub=self._constraint_coefs, b_ub=self._constraint_bounds)
        return result
