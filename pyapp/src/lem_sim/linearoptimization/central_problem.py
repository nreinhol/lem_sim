import numpy as np


class CentralProblem(object):

    def __init__(self):
        self._target_coefs = np.array([-1, -2, -1, -3])  # cost vectors
        self._individual_resources = np.array([4, 9])  # individual resources
        self._shared_resources = np.array([8, 5])  # shared resources
        self._individual_coefs = np.array([[2, 1, 0, 0], [0, 0, 2, 3]])  # individual coefficients
        self._shared_coefs = np.array([[1, 3, 2, 1], [1, 1, 1, 1]])  # shared coefficients

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

    @property
    def shared_coefs(self):
        return self._shared_coefs

    def show(self):
        print('Target Coefficients:\n', self._target_coefs)
        print('Individual Coefficients:', *self._individual_coefs, sep='\n')
        print('Individual Resources:\n', self._individual_resources)
        print('Shared Coefficients:', *self._shared_coefs, sep='\n')
        print('Shared Resources:\n', self._shared_resources)
