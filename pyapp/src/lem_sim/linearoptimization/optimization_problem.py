from scipy.optimize import linprog
import numpy as np


class OptimizationProblem(object):

    def __init__(self, target_coefs, individual_resources, individual_coefs, shared_resources, shared_coefs):
        self._target_coefs = target_coefs  # cost vectors
        self._individual_resources = individual_resources  # individual resources
        self._shared_resources = shared_resources  # shared resources
        self._individual_coefs = individual_coefs  # individual coefficients
        self._shared_coefs = shared_coefs  # shared coefficients

    @property
    def target_coefs(self):
        return self._target_coefs

    @property
    def individual_resources(self):
        return self._individual_resources

    @property
    def individual_coefs(self):
        return self._individual_coefs

    @property
    def shared_resources(self):
        return self._shared_resources

    @shared_resources.setter
    def shared_resources(self, value):
        self._shared_resources = value

    @property
    def shared_coefs(self):
        return self._shared_coefs

    def solve(self):
        constraint_coefs = np.concatenate((self._individual_coefs, self._shared_coefs))
        constraint_resources = np.concatenate((self._individual_resources, self._shared_resources))

        return linprog(self._target_coefs, constraint_coefs, constraint_resources)

    def show(self):
        print('Target Coefficients:\n', self._target_coefs)
        print('Individual Coefficients:', *self._individual_coefs, sep='\n')
        print('Individual Resources:\n', self._individual_resources)
        print('Shared Coefficients:', *self._shared_coefs, sep='\n')
        print('Shared Resources:\n', self._shared_resources)

    def __str__(self):
        class_str = 'Target Coefficients:\n{}\nIndividual Coefficients:\n{}\nIndividual Resources:\n{}\nShared Coefficients:\n{}\nShared Resources:\n{}'.format(
            self._target_coefs,
            self._individual_coefs,
            self._individual_resources,
            self._shared_coefs,
            self._shared_resources
        )

        return class_str
