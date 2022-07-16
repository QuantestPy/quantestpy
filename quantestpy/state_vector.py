import unittest
import numpy as np
import qiskit
from typing import Union
import decimal
from quantestpy.exceptions import QuantestPyError, QuantestPyAssertionError

ut_test_case = unittest.TestCase()


def assert_is_normalized(
        state_vector_subject_to_test: Union[
            np.ndarray,
            list,
            qiskit.quantum_info.states.statevector.Statevector],
        significant_figure: int = 5,
        msg=None) -> None:

    a = state_vector_subject_to_test

    # check type
    if not isinstance(a, np.ndarray) and not isinstance(a, list) and not \
            isinstance(a, qiskit.quantum_info.states.statevector.Statevector):
        raise TypeError(
            "The type of state_vector_subject_to_test must be "
            "either numpy.ndarray, list or "
            "qiskit.quantum_info.states.statevector.Statevector."
        )

    # conv. list to ndarray
    if not isinstance(a, np.ndarray):
        a = np.array(a)

    # calc. norm
    norm = np.sqrt(np.dot(a, a.conj()).real)
    decimal.getcontext().prec = significant_figure
    norm_round = +decimal.Decimal(norm)

    if norm_round == 1.:
        return
    else:
        error_msg = ("The state vector is not normalized.\n"
                     f"Norm: {norm_round}")
        msg = ut_test_case._formatMessage(msg, error_msg)
        raise QuantestPyAssertionError(msg)


def assert_equal(
        state_vector_subject_to_test: Union[np.ndarray, list],
        state_vector_expected: Union[np.ndarray, list],
        significant_figure: int = 8,
        msg=None):

    a = state_vector_subject_to_test
    b = state_vector_expected

    # check type
    if not isinstance(a, np.ndarray) and not isinstance(a, list):
        raise TypeError(
            "The type of state_vector_subject_to_test must be either "
            "numpy.ndarray or list."
        )

    if not isinstance(b, np.ndarray) and not isinstance(b, list):
        raise TypeError(
            "The type of state_vector_expected must be either"
            "numpy.ndarray or list."
        )

    # conv. list to ndarray
    if isinstance(a, list):
        a = np.array(a)

    if isinstance(b, list):
        b = np.array(b)

    # check shape
    if a.shape != b.shape:
        raise QuantestPyError(
            "The shape of state_vector_subject_to_test must be "
            "identical to that of state_vector_expected."
        )

    #
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
