import unittest
import numpy as np
from typing import Union


ut_test_case = unittest.TestCase()


def assert_is_normalized(
        state_vector_subject_to_test: Union[np.ndarray, list],
        torelance: int = 5,
        msg=None) -> None:

    a = state_vector_subject_to_test.copy()

    # check type
    if not isinstance(a, np.ndarray) and not isinstance(a, list):
        raise TypeError(
            "The type of state_vector_subject_to_test must be "
            "either numpy.ndarray or list."
        )

    # conv. list to ndarray
    if isinstance(a, list):
        a = np.array(a)

    # calc. norm
    norm = np.sqrt((a * a.conj()).sum().real)
    norm_round = np.round(norm, decimals=torelance)

    if norm_round == 1.:
        return
    else:
        error_msg = "The state vector is not normalized. \n" + \
            f"Norm: {norm_round}"
        msg = ut_test_case._formatMessage(msg, error_msg)
        raise ut_test_case.failureException(msg)
