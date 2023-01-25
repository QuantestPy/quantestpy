import unittest
from typing import Union

import numpy as np

from quantestpy.assertion.assert_equivalent_state_vectors import \
    _remove_global_phase_from_two_vectors
from quantestpy.exceptions import QuantestPyAssertionError, QuantestPyError

ut_test_case = unittest.TestCase()


def _get_matrix_norm(
        a: np.ndarray,
        b: np.ndarray,
        matrix_norm_type: str,
        up_to_global_phase: bool) -> float:

    if up_to_global_phase:
        a_shape = a.shape

        # cvt. to vector
        a = np.ravel(a)
        b = np.ravel(b)

        # rm. global phase
        a, b = _remove_global_phase_from_two_vectors(a, b)

        # back to matrix
        a = np.reshape(a, newshape=a_shape)
        b = np.reshape(b, newshape=a_shape)

    m = a - b

    if matrix_norm_type == "operator_norm_1":
        matrix_norm_value = np.linalg.norm(m, 1)

    elif matrix_norm_type == "operator_norm_2":
        matrix_norm_value = np.linalg.norm(m, 2)

    elif matrix_norm_type == "operator_norm_inf":
        matrix_norm_value = np.linalg.norm(m, np.inf)

    elif matrix_norm_type == "Frobenius_norm":
        matrix_norm_value = np.linalg.norm(m, "fro")

    elif matrix_norm_type == "max_norm":
        matrix_norm_value = np.max(np.abs(m))

    else:
        raise

    return matrix_norm_value


def assert_equivalent_operators(
        operator_a: Union[np.ndarray, np.matrix],
        operator_b: Union[np.ndarray, np.matrix],
        rtol: float = 0.,
        atol: float = 1e-8,
        up_to_global_phase: bool = False,
        matrix_norm_type: Union[str, None] = None,
        msg=None) -> None:

    a = operator_a
    b = operator_b

    # conv. list to ndarray
    if not isinstance(a, np.ndarray):
        a = np.array(a)

    if not isinstance(b, np.ndarray):
        b = np.array(b)

    # check shape
    if a.shape != b.shape:
        raise QuantestPyError(
            "The shapes of the operators must be the same."
        )

    # remove global phase
    if up_to_global_phase:
        a_shape = a.shape

        # cvt. to vector
        a = np.ravel(a)
        b = np.ravel(b)

        # rm. global phase
        a, b = _remove_global_phase_from_two_vectors(a, b)

        # cvt. back to matrix
        a = np.reshape(a, newshape=a_shape)
        b = np.reshape(b, newshape=a_shape)

    # assert equal
    if matrix_norm_type is None:

        try:
            np.testing.assert_allclose(
                actual=a,
                desired=b,
                rtol=rtol,
                atol=atol,
                err_msg=f"Up to global phase: {up_to_global_phase}"
            )

        except AssertionError as e:
            error_msg = e.args[0]
            msg = ut_test_case._formatMessage(msg, error_msg)
            raise QuantestPyAssertionError(msg)

    else:
        # assert check matrix norm as a distance
        matrix_norm_a_minus_b = _get_matrix_norm(
            a,
            b,
            matrix_norm_type,
            up_to_global_phase
        )

        if rtol != 0.:
            matrix_norm_b = _get_matrix_norm(
                b,
                np.zeros_like(b),
                matrix_norm_type,
                False
            )

        else:
            matrix_norm_b = 0.

        if matrix_norm_a_minus_b >= atol + rtol * matrix_norm_b:

            error_msg = "matrix norm ||A-B|| " \
                + format(matrix_norm_a_minus_b, ".15g") \
                + " is larger than (atol + rtol*||B||) " \
                + format(atol + rtol * matrix_norm_b, ".15g") + "."
            msg = ut_test_case._formatMessage(msg, error_msg)
            raise QuantestPyAssertionError(msg)
