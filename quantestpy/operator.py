import unittest
import numpy as np
from typing import Union
from quantestpy.exceptions import QuantestPyError, QuantestPyAssertionError
from quantestpy import state_vector

ut_test_case = unittest.TestCase()


def assert_is_unitary(
        operator_subject_to_test: Union[np.ndarray, np.matrix],
        number_of_decimal_places: int = 5,
        msg=None) -> None:

    m = operator_subject_to_test

    # conv. list to matrix
    if not isinstance(m, np.matrix):
        m = np.matrix(m)

    a = m * m.H
    a = np.round(a, decimals=number_of_decimal_places)

    if np.all(a == np.eye(m.shape[0])):
        return

    else:
        error_msg = ("Operator is not unitary.\n"
                     f"m * m^+:\n{a}")
        msg = ut_test_case._formatMessage(msg, error_msg)
        raise QuantestPyAssertionError(msg)


def assert_equal(
        operator_a: Union[np.ndarray, np.matrix],
        operator_b: Union[np.ndarray, np.matrix],
        rtol: float = 0.,
        atol: float = 1e-8,
        up_to_global_phase: bool = False,
        msg=None) -> None:

    a = operator_a
    b = operator_b

    # conv. list to ndarray
    if not isinstance(a, np.ndarray):
        a = np.array(a)

    if not isinstance(b, np.ndarray):
        b = np.array(b)

    # check shape
    if a.shape != b.shape:
        raise QuantestPyError(
            "The shapes of the operators must be the same."
        )

    # cvt. to vector
    a = np.ravel(a)
    b = np.ravel(b)

    # Note: error message dhould
    state_vector.assert_equal(a, b, rtol, atol, up_to_global_phase, msg)
