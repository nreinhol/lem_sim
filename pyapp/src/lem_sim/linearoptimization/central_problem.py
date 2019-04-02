import numpy as np


class CentralProblem:

    def __init__(self):
        self._target_coefs = np.array([1, -2, -1, -3])  # this list represents the sum of agents cost vectors
        self._individual_resources = np.array([[4], [9]])  # agents individual resources
        self._individual_coefs = np.array([[2], [1], [2], [3]])  # agents individual coefficients
        self._shared_resources = np.array([[8], [5]])  # agents shared resources
        self._shared_coefs = np.array([[1, 1], [3, 1], [2, 1], [1, 1]])  # agents shared coefficients

    @property
    def target_coefs(self):
        return self._target_coefs

    @target_coefs.setter
    def target_coefs(self, values):
        self._target_coefs = values

    @property
    def individual_resources(self):
        return self._individual_resources

    @individual_resources.setter
    def individual_resources(self, values):
        self._individual_resources = values

    @property
    def individual_coefs(self):
        return self._individual_coefs

    @individual_coefs.setter
    def individual_coefs(self, values):
        self._individual_coefs = values

    @property
    def shared_resources(self):
        return self._shared_resources

    @shared_resources.setter
    def shared_resources(self, values):
        self._shared_resources = values

    @property
    def shared_coefs(self):
        return self._shared_resources

    @shared_coefs.setter
    def shared_coefs(self, values):
        self._shared_resources = values
