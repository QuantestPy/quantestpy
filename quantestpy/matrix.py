import unittest
import numpy as np
import qiskit
from typing import Union
from quantestpy.exceptions import QuantestPyError, QuantestPyAssertionError
from quantestpy import state_vector

ut_test_case = unittest.TestCase()


def assert_is_unitary(
        matrix_subject_to_test: Union[
            np.ndarray,
            np.matrix,
            qiskit.quantum_info.operators.operator.Operator],
        number_of_decimal_places: int = 5,
        msg=None) -> None:

    m = matrix_subject_to_test

    # conv. list to matrix
    if not isinstance(m, np.matrix):
        m = np.matrix(m)

    a = m * m.H
    a = np.round(a, decimals=number_of_decimal_places)

    if np.all(a == np.eye(m.shape[0])):
        return

    else:
        error_msg = ("Matrix is not unitary.\n"
                     f"m * m^+:\n{a}")
        msg = ut_test_case._formatMessage(msg, error_msg)
        raise QuantestPyAssertionError(msg)


def assert_equal(
        matrix_a: Union[
            np.ndarray,
            qiskit.quantum_info.operators.operator.Operator],
        matrix_b: Union[
            np.ndarray,
            list,
            qiskit.quantum_info.operators.operator.Operator],
        number_of_decimal_places: int = 5,
        check_including_global_phase: bool = True,
        msg=None) -> None:

    a = matrix_a
    b = matrix_b

    # conv. list to ndarray
    if not isinstance(a, np.ndarray):
        a = np.array(a)

    if not isinstance(b, np.ndarray):
        b = np.array(b)

    # check shape
    if a.shape != b.shape:
        raise QuantestPyError(
            "The shapes of the matrices must be the same."
        )

    # conv. to vector
    a = np.ravel(a)
    b = np.ravel(b)

    # Note: error message dhould
    state_vector.assert_equal(a, b, number_of_decimal_places,
                              check_including_global_phase, msg)
