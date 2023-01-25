import unittest
from typing import Union

import numpy as np

from quantestpy.exceptions import QuantestPyAssertionError

ut_test_case = unittest.TestCase()


def assert_unitary_operator(
        operator_subject_to_test: Union[np.ndarray, np.matrix],
        atol: float = 1e-8,
        msg=None) -> None:

    m = operator_subject_to_test

    # conv. list to matrix
    if not isinstance(m, np.matrix):
        m = np.matrix(m)

    a = m * m.H

    if np.all(np.abs(a - np.eye(m.shape[0])) <= atol):
        return

    else:
        error_msg = ("Operator is not unitary.\n"
                     f"m * m^+:\n{a}")
        msg = ut_test_case._formatMessage(msg, error_msg)
        raise QuantestPyAssertionError(msg)
