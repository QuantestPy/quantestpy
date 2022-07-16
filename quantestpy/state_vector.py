import unittest
import numpy as np
import qiskit
from typing import Union
import decimal
from decimal import Decimal
from quantestpy.exceptions import QuantestPyError, QuantestPyAssertionError

ut_test_case = unittest.TestCase()


def assert_is_normalized(
        state_vector_subject_to_test: Union[
            np.ndarray,
            list,
            qiskit.quantum_info.states.statevector.Statevector],
        number_of_decimal_places: int = 5,
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

    decimal.getcontext().prec = 28
    twoplaces = Decimal(10) ** (-number_of_decimal_places)
    norm_round = Decimal(norm).quantize(twoplaces)

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
        number_of_decimal_places: int = 5,
        check_including_global_phase: bool = True,
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
    if not check_including_global_phase:
        a_global_phase = a[0] / abs(a[0])
        a = a * a_global_phase.conj()

        b_global_phase = b[0] / abs(b[0])
        b = b * b_global_phase.conj()

    #
    decimal.getcontext().prec = 28
    twoplaces = Decimal(10) ** (-number_of_decimal_places)

    for i, a_element in enumerate(a):
        b_element = b[i]

        a_element_real = Decimal(a_element.real).quantize(twoplaces)
        b_element_real = Decimal(b_element.real).quantize(twoplaces)

        if a_element_real != b_element_real:
            error_msg = (
                f"Real part of {i} th element are not equal:\n"
                f"{a_element_real}\n"
                f"{b_element_real}"
            )
            msg = ut_test_case._formatMessage(msg, error_msg)
            raise QuantestPyAssertionError(msg)

        a_element_imag = Decimal(a_element.imag).quantize(twoplaces)
        b_element_imag = Decimal(b_element.imag).quantize(twoplaces)

        if a_element_imag != b_element_imag:
            error_msg = (
                f"Imaginary part of {i} th element are not equal:\n"
                f"{a_element_imag}\n"
                f"{b_element_imag}"
            )
            msg = ut_test_case._formatMessage(msg, error_msg)
            raise QuantestPyAssertionError(msg)

    return
