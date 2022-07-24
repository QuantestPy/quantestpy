import unittest


class QuantestPyError(unittest.TestCase.failureException):
    pass


class QuantestPyAssertionError(QuantestPyError):
    pass


class QuantestPyTestCircuitError(Exception):
    pass
