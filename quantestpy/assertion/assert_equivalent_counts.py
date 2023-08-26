import unittest
from typing import Dict, Union

import numpy as np

from quantestpy.exceptions import QuantestPyAssertionError

ut_test_case = unittest.TestCase()


def assert_equivalent_counts(
        counts_a: Dict[str, int],
        counts_b: Dict[str, int],
        sigma: Union[float, int] = 2.,
        msg=None) -> None:

    if not isinstance(counts_a, dict) or not isinstance(counts_b, dict):
        raise TypeError(
            "The type of counts must be dict."
        )

    if not isinstance(sigma, float) and not isinstance(sigma, int):
        raise TypeError(
            "The type of sigma must be float or int."
        )

    for k, v in counts_a.items():
        if not isinstance(k, str):
            raise TypeError(
                "The type of key in counts must be str."
            )
        if not isinstance(v, int):
            raise TypeError(
                "The type of value in counts must be int."
            )
        if v < 0:
            raise ValueError(
                "The value in counts must be non-negative."
            )

    for k, v in counts_b.items():
        if not isinstance(k, str):
            raise TypeError(
                "The type of key in counts must be str."
            )
        if not isinstance(v, int):
            raise TypeError(
                "The type of value in counts must be int."
            )
        if v < 0:
            raise ValueError(
                "The value in counts must be non-negative."
            )

    if len(counts_a) != len(counts_b):
        err_msg = "The number of keys in counts are not the same."
        msg = ut_test_case._formatMessage(msg, err_msg)
        raise QuantestPyAssertionError(msg)

    for k in counts_a.keys():
        if k in counts_b.keys():
            v_a = counts_a[k]
            v_b = counts_b[k]
            err_a = np.sqrt(v_a)
            err_b = np.sqrt(v_b)

            diff = np.abs(v_a - v_b)
            tole = (err_a + err_b) * sigma
            if diff > tole:
                err_msg = f"The values of key {k} are too different.\n" \
                    f"counts_a[{k}] = {v_a}, counts_b[{k}] = {v_b}.\n" \
                    f"Difference: {diff}\nTolerance: {int(tole)}."
                msg = ut_test_case._formatMessage(msg, err_msg)
                raise QuantestPyAssertionError(msg)

        else:
            err_msg = f"The key {k} in counts_a is not in counts_b."
            msg = ut_test_case._formatMessage(msg, err_msg)
            raise QuantestPyAssertionError(msg)

    return None
