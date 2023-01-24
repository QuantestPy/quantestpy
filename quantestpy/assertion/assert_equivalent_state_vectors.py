import unittest
from typing import Union

import numpy as np

from quantestpy.exceptions import QuantestPyAssertionError, QuantestPyError

ut_test_case = unittest.TestCase()


def _remove_global_phase_from_two_vectors(a: np.ndarray, b: np.ndarray):

    abs_a = np.abs(a)
    max_value_abs_a = np.max(abs_a)
    max_index_abs_a = np.argmax(abs_a)
    a_global_phase = a[max_index_abs_a] / max_value_abs_a

    a = a * a_global_phase.conj()

    b_global_phase = b[max_index_abs_a] / abs(b[max_index_abs_a])

    b = b * b_global_phase.conj()

    return a, b


def assert_equivalent_state_vectors(
        state_vector_a: Union[np.ndarray, list],
        state_vector_b: Union[np.ndarray, list],
        rtol: float = 0.,
        atol: float = 1e-8,
        up_to_global_phase: bool = False,
        msg=None):

    a = state_vector_a
    b = state_vector_b

    # check type
    if not isinstance(a, np.ndarray) and not isinstance(a, list):
        raise TypeError(
            "The type of state_vector must be either numpy.ndarray or list."
        )

    if not isinstance(b, np.ndarray) and not isinstance(b, list):
        raise TypeError(
            "The type of state_vector must be either numpy.ndarray or list."
        )

    # cvt. list to ndarray
    if not isinstance(a, np.ndarray):
        a = np.array(a)

    if not isinstance(b, np.ndarray):
        b = np.array(b)

    # check shape
    if a.shape != b.shape:
        raise QuantestPyError(
            "The shapes of the state_vectors must be the same."
        )

    # remove global phase
    if up_to_global_phase:
        a, b = _remove_global_phase_from_two_vectors(a, b)

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
