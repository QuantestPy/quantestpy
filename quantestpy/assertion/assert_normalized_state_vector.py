import unittest
from typing import Union

import numpy as np

from quantestpy.exceptions import QuantestPyAssertionError

ut_test_case = unittest.TestCase()


def assert_normalized_state_vector(
        state_vector_subject_to_test: Union[np.ndarray, list],
        atol: float = 1e-8,
        msg=None) -> None:

    a = state_vector_subject_to_test

    # check type
    if not isinstance(a, np.ndarray) and not isinstance(a, list):
        raise TypeError(
            "The type of state_vector_subject_to_test must be "
            "either numpy.ndarray or list."
        )

    # conv. list to ndarray
    if not isinstance(a, np.ndarray):
        a = np.array(a)

    # calc. norm
    norm = np.sqrt(np.dot(a, a.conj()).real)

    if np.abs(norm - 1.) <= atol:
        return
    else:
        error_msg = ("The state vector is not normalized.\n"
                     f"Norm: {norm}")
        msg = ut_test_case._formatMessage(msg, error_msg)
        raise QuantestPyAssertionError(msg)
