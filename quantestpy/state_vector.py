import unittest
import numpy as np
from typing import Union
from quantestpy.exceptions import QuantestPyError
from quantestpy.util import shape_message
import re

ut_test_case = unittest.TestCase()


def assert_is_normalized(
        state_vector_subject_to_test: Union[np.ndarray, list],
        torelance: int = 5,
        msg=None) -> None:

    a = state_vector_subject_to_test

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


def assert_equal(
        state_vector_subject_to_test: Union[np.ndarray, list],
        state_vector_expected: Union[np.ndarray, list],
        absolute_torelance_decimals: int = 8,
        determine_torelance_from_state_vector_expected: bool = False,
        msg=None):

    a = state_vector_subject_to_test
    b = state_vector_expected

    # check type
    if not isinstance(a, np.ndarray) and not isinstance(a, list):
        msg = shape_message(
            ["The type of state_vector_subject_to_test must be either",
             "numpy.ndarray or list."]
        )
        raise TypeError(msg)

    if not isinstance(b, np.ndarray) and not isinstance(b, list):
        msg = shape_message(
            ["The type of state_vector_expected must be either",
             "numpy.ndarray or list."]
        )
        raise TypeError(msg)

    # conv. list to ndarray
    if isinstance(a, list):
        a = np.array(a)

    if isinstance(b, list):
        b = np.array(b)

    # check shape
    if a.shape != b.shape:
        raise QuantestPyError(
            ["The shape of state_vector_subject_to_test must be "
             "identical to that of state_vector_expected."]
        )

    #
    if determine_torelance_from_state_vector_expected:

        def _derive_effective_decimals(value: float):
            pattern = r"\.{1}\d*"
            result = re.search(pattern, str(value))
            try:
                effective_decimals = len(result.group(0)) - 1
            except AttributeError:
                effective_decimals = 1
            return effective_decimals

        for i, a_element in enumerate(a):
            b_element = b[i]
            b_elm_real = b_element.real
            effective_decimals = _derive_effective_decimals(b_elm_real)
            a_elm_real = np.round(a_element.real, effective_decimals)
            if b_elm_real != a_elm_real:
                error_msg = shape_message(
                    [f"{i}th vector real components are not equal:\n",
                     f"Actual: {a_elm_real}\n",
                     f"Expected: {b_elm_real}"]
                )
                msg = ut_test_case._formatMessage(msg, error_msg)
                raise ut_test_case.failureException(msg)

            b_elm_imag = b_element.imag
            effective_decimals = _derive_effective_decimals(b_elm_imag)
            a_elm_imag = np.round(a_element.imag, effective_decimals)
            if b_elm_imag != a_elm_imag:
                error_msg = f"{i}th vector imaginary components are not " + \
                    "equal:\n" + \
                    f"Actual: {a_elm_imag}\n" + \
                    f"Expected: {b_elm_imag}"
                msg = ut_test_case._formatMessage(msg,
                                                  error_msg)
                raise ut_test_case.failureException(msg)

    else:
        if not np.allclose(
                a, b, rtol=0., atol=10**(-absolute_torelance_decimals)):
            error_msg = shape_message(
                ["The two vectors are not equal:\n",
                 f"Actual: {a}\n",
                 f"Expected: {b}"]
            )
            msg = ut_test_case._formatMessage(msg, error_msg)
            raise ut_test_case.failureException(msg)

    return
