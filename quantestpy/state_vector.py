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
        state_vector_a: Union[
            np.ndarray,
            list,
            qiskit.quantum_info.states.statevector.Statevector],
        state_vector_b: Union[
            np.ndarray,
            list,
            qiskit.quantum_info.states.statevector.Statevector],
        significant_figure: int = 5,
        msg=None):

    a = state_vector_a
    b = state_vector_b

    # check type
    if not isinstance(a, np.ndarray) and not isinstance(a, list) and not \
            isinstance(a, qiskit.quantum_info.states.statevector.Statevector):
        raise TypeError(
            "The type of state_vector must be either numpy.ndarray, list or "
            "qiskit.quantum_info.states.statevector.Statevector."
        )

    if not isinstance(b, np.ndarray) and not isinstance(b, list) and not \
            isinstance(b, qiskit.quantum_info.states.statevector.Statevector):
        raise TypeError(
            "The type of state_vector must be either numpy.ndarray. list or "
            "qiskit.quantum_info.states.statevector.Statevector."
        )

    # conv. list to ndarray
    if not isinstance(a, np.ndarray):
        a = np.array(a)

    if not isinstance(b, np.ndarray):
        b = np.array(b)

    # check shape
    if a.shape != b.shape:
        raise QuantestPyError(
            "The shapes of the state_vectors must be the same."
        )

    #
    decimal.getcontext().prec = significant_figure
    for i, a_element in enumerate(a):
        b_element = b[i]

        a_element_real = +decimal.Decimal(a_element.real)
        b_element_real = +decimal.Decimal(b_element.real)

        if a_element_real != b_element_real:
            error_msg = (
                f"Real part of {i} th element are not equal:\n"
                f"{a_element_real}\n"
                f"{b_element_real}"
            )
            msg = ut_test_case._formatMessage(msg, error_msg)
            raise QuantestPyAssertionError(msg)

        a_element_imag = +decimal.Decimal(a_element.imag)
        b_element_imag = +decimal.Decimal(b_element.imag)

        if a_element_imag != b_element_imag:
            error_msg = (
                f"Imaginary part of {i} th element are not equal:\n"
                f"{a_element_imag}\n"
                f"{b_element_imag}"
            )
            msg = ut_test_case._formatMessage(msg, error_msg)
            raise QuantestPyAssertionError(msg)

    return
