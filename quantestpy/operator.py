import unittest
import numpy as np
from typing import Union
from quantestpy.exceptions import QuantestPyError, QuantestPyAssertionError
from quantestpy.state_vector import _remove_global_phase_from_two_vectors

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

    # remove global phase
    if up_to_global_phase:
        a_shape = a.shape

        # cvt. to vector
        a = np.ravel(a)
        b = np.ravel(b)

        # rm. global phase
        a, b = _remove_global_phase_from_two_vectors(a, b)

        # cvt. back to matrix
        a = np.reshape(a, newshape=a_shape)
        b = np.reshape(b, newshape=a_shape)

    # assert equal
    try:
        np.testing.assert_allclose(
            actual=a,
            desired=b,
            rtol=rtol,
            atol=atol,
            err_msg=f"Up to global phase: {up_to_global_phase}"
        )

    except AssertionError as e:
        error_msg = e.args[0]
        msg = ut_test_case._formatMessage(msg, error_msg)
        raise QuantestPyAssertionError(msg)
