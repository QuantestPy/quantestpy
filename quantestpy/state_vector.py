import unittest
import numpy as np
from typing import Union
from quantestpy.exceptions import QuantestPyError, QuantestPyAssertionError

ut_test_case = unittest.TestCase()


def assert_is_normalized(
        state_vector_subject_to_test: Union[np.ndarray, list],
        number_of_decimal_places: int = 5,
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
    norm_round = np.round(norm, decimals=number_of_decimal_places)

    if norm_round == 1.:
        return
    else:
        error_msg = ("The state vector is not normalized.\n"
                     f"Norm: {norm_round}")
        msg = ut_test_case._formatMessage(msg, error_msg)
        raise QuantestPyAssertionError(msg)


def assert_equal(
        state_vector_a: Union[np.ndarray, list],
        state_vector_b: Union[np.ndarray, list],
        number_of_decimal_places: int = 5,
        check_including_global_phase: bool = True,
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
    if not check_including_global_phase:

        for i in range(len(a)):
            if abs(a[i]) > 0.:
                a_global_phase = a[i] / abs(a[i])
                break

        a = a * a_global_phase.conj()

        for i in range(len(b)):
            if abs(b[i]) > 0.:
                b_global_phase = b[i] / abs(b[i])
                break

        b = b * b_global_phase.conj()

    # round
    a = np.round(a, decimals=number_of_decimal_places)
    b = np.round(b, decimals=number_of_decimal_places)

    # assert equal
    equals = a == b
    if np.all(equals):
        return

    error_msgs = list()
    for i, equal in enumerate(equals):
        if not equal:
            error_msgs.append((
                f"\n{i}th element:\n"
                f"a: {a[i]}\n"
                f"b: {b[i]}"
            ))
    error_msg = "".join(error_msgs)
    msg = ut_test_case._formatMessage(msg, error_msg)
    raise QuantestPyAssertionError(msg)
