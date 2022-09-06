import unittest
import numpy as np
from typing import Union
import itertools
import traceback
import re
from qiskit import QuantumCircuit

from quantestpy import operator
from quantestpy import TestCircuit
from quantestpy.exceptions import QuantestPyError, QuantestPyAssertionError
from quantestpy.converter import _cvt_qiskit_to_test_circuit
from quantestpy.converter import _cvt_openqasm_to_test_circuit
from quantestpy.state_vector import _remove_global_phase_from_two_vectors

ut_test_case = unittest.TestCase()


def assert_equal_to_operator(
        operator_: Union[np.ndarray, np.matrix],
        qasm: str = None,
        qiskit_circuit: QuantumCircuit = None,
        test_circuit: TestCircuit = None,
        from_right_to_left_for_qubit_ids: bool = False,
        number_of_decimal_places: int = 5,
        up_to_global_phase: bool = False,
        msg=None) -> None:

    if qasm is None and qiskit_circuit is None and test_circuit is None:
        raise QuantestPyError(
            "Missing qasm or qiskit_circuit or test circuit."
        )

    if (qasm is not None and qiskit_circuit is not None) \
            or (qasm is not None and test_circuit is not None) \
            or (qiskit_circuit is not None and test_circuit is not None):
        raise QuantestPyError(
            "You need to choose one parameter of Qasm, \
                qiskit_circuit and test circuit."
        )

    if qasm is not None:
        test_circuit = _cvt_openqasm_to_test_circuit(qasm)

    if qiskit_circuit is not None:
        test_circuit = _cvt_qiskit_to_test_circuit(qiskit_circuit)

    test_circuit._from_right_to_left_for_qubit_ids = \
        from_right_to_left_for_qubit_ids

    operator_from_test_circuit = test_circuit._get_whole_gates()

    operator.assert_equal(
        operator_from_test_circuit,
        operator_,
        number_of_decimal_places,
        up_to_global_phase,
        msg)


def assert_is_zero(qasm: str = None,
                   qiskit_circuit: QuantumCircuit = None,
                   test_circuit: TestCircuit = None,
                   qubits: list = None,
                   a_tol: float = 1e-8,
                   msg=None) -> None:

    # Memo220805JN: the following input checker may be common for the other
    # functions in this module, thus can be one function.
    if qasm is None and qiskit_circuit is None and test_circuit is None:
        raise QuantestPyError(
            "Missing qasm or qiskit_circuit or test circuit."
        )

    if (qasm is not None and qiskit_circuit is not None) \
            or (qasm is not None and test_circuit is not None) \
            or (qiskit_circuit is not None and test_circuit is not None):
        raise QuantestPyError(
            "You need to choose one parameter of Qasm, \
                qiskit_circuit and test circuit."
        )

    if qasm is not None:
        test_circuit = _cvt_openqasm_to_test_circuit(qasm)

    if qiskit_circuit is not None:
        test_circuit = _cvt_qiskit_to_test_circuit(qiskit_circuit)

    if not isinstance(qubits, list) and qubits is not None:
        raise QuantestPyError(
            "qubits must be a list of integer(s) as qubit's ID(s)."
        )

    state_vec = test_circuit._get_state_vector()
    num_qubit = test_circuit._num_qubit
    if qubits is None:
        qubits = [i for i in range(num_qubit)]

    def _assert_is_zero_for_one_qubit(qubit: int) -> bool:

        if qubit > num_qubit-1:
            raise QuantestPyError(
                f"qubit {qubit} is out of range for the given circuit."
            )

        dim_reg_front = 2**qubit
        dim_reg_rear = 2**(num_qubit - qubit - 1)

        for i in range(dim_reg_front):
            clipped_state_vec = \
                state_vec[i*dim_reg_rear*2: (i+1)*dim_reg_rear*2]
            clipped_state_vec = clipped_state_vec[dim_reg_rear:]

            if not np.all(clipped_state_vec < a_tol):
                return True  # = assertion error

        return False  # = assertion non-error

    error_qubits = []
    for qubit in qubits:
        if _assert_is_zero_for_one_qubit(qubit):
            error_qubits.append(qubit)

    if len(error_qubits) > 0:
        error_msg = f"qubit(s) {error_qubits} are either non-zero or " \
            + "entangled with other qubits."
        msg = ut_test_case._formatMessage(msg, error_msg)
        raise QuantestPyAssertionError(msg)


def assert_ancilla_is_zero(ancilla_qubits: list,
                           qasm: str = None,
                           qiskit_circuit: QuantumCircuit = None,
                           test_circuit: TestCircuit = None,
                           a_tol: float = 1e-8,
                           msg=None) -> None:

    if qasm is None and qiskit_circuit is None and test_circuit is None:
        raise QuantestPyError(
            "Missing qasm or qiskit_circuit or test circuit."
        )

    if (qasm is not None and qiskit_circuit is not None) \
            or (qasm is not None and test_circuit is not None) \
            or (qiskit_circuit is not None and test_circuit is not None):
        raise QuantestPyError(
            "You need to choose one parameter of Qasm, \
                qiskit_circuit and test circuit."
        )

    if qasm is not None:
        test_circuit = _cvt_openqasm_to_test_circuit(qasm)

    if qiskit_circuit is not None:
        test_circuit = _cvt_qiskit_to_test_circuit(qiskit_circuit)

    if not isinstance(ancilla_qubits, list):
        raise QuantestPyError(
            "ancilla_qubits must be a list of integer(s) as qubit's ID(s)."
        )

    num_qubit = test_circuit._num_qubit

    # system qubits <=> ancilla qubits
    system_qubits = [qubit for qubit in range(num_qubit)
                     if qubit not in ancilla_qubits]

    def _add_x_gate_in_front(gates: list, qubit: int) -> dict:
        x_gate = {"name": "x",
                  "target_qubit": [qubit],
                  "control_qubit": [],
                  "control_value": [],
                  "parameter": []}
        gates.insert(0, x_gate)

    all_combinations_of_system_qubits = []
    for size in range(len(system_qubits)+1):
        c = list(itertools.combinations(system_qubits, size))
        all_combinations_of_system_qubits += c

    error_msgs_from_assert_is_zero = []
    for comb_of_sys_qubits in all_combinations_of_system_qubits:

        # add x gate(s) in test_circuit
        for system_qubit in comb_of_sys_qubits:
            _add_x_gate_in_front(test_circuit._gates, system_qubit)

        # assertion using assert_is_zero
        try:
            assert_is_zero(test_circuit=test_circuit,
                           qubits=ancilla_qubits,
                           a_tol=a_tol)

        except QuantestPyAssertionError as e:
            t = traceback.format_exception_only(type(e), e)[0]
            error_msgs_from_assert_is_zero.append(t)

        # remove x gate(s) from test_circuit, i.e. reset test_circuit.
        for _ in comb_of_sys_qubits:
            del test_circuit._gates[0]

    if len(error_msgs_from_assert_is_zero) == 0:
        return None  # = assertion non-error

    error_qubits = []
    for err_m_from_assert_is_zero in list(set(error_msgs_from_assert_is_zero)):
        error_qubits_str_list = re.findall(r'\d+', err_m_from_assert_is_zero)

        for error_qubit_str in error_qubits_str_list:
            error_qubits.append(int(error_qubit_str))

    error_qubits = list(set(error_qubits))

    error_msg = f"qubit(s) {error_qubits} are either non-zero or " \
        + "entangled with other qubits."
    msg = ut_test_case._formatMessage(msg, error_msg)
    raise QuantestPyAssertionError(msg)


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


def assert_equal(
        qasm_a: Union[str, None] = None,
        qiskit_circuit_a: Union[QuantumCircuit, None] = None,
        test_circuit_a: Union[TestCircuit, None] = None,
        qasm_b: Union[str, None] = None,
        qiskit_circuit_b: Union[QuantumCircuit, None] = None,
        test_circuit_b: Union[TestCircuit, None] = None,
        number_of_decimal_places: int = 5,
        up_to_global_phase: bool = False,
        matrix_norm_type: Union[str, None] = None,
        tolerance_for_matrix_norm_value: Union[float, None] = None,
        msg: Union[str, None] = None):

    # Check inputs for circuit A
    if qasm_a is None and qiskit_circuit_a is None and test_circuit_a is None:
        raise QuantestPyError(
            "Missing information for circuit A. "
            "One of the following must be given: "
            "qasm_a, qiskit_circuit_a and test_circuit_a."
        )

    if (qasm_a is not None and qiskit_circuit_a is not None) \
            or (qasm_a is not None and test_circuit_a is not None) \
            or (qiskit_circuit_a is not None and test_circuit_a is not None):
        raise QuantestPyError(
            "Too much information for circuit A. "
            "Only one of the following should be given: "
            "qasm_a, qiskit_circuit_a and test_circuit_a."
        )

    if qasm_a is not None and not isinstance(qasm_a, str):
        raise QuantestPyError(
            "Type of qasm_a must be str."
        )

    if qiskit_circuit_a is not None \
            and not isinstance(qiskit_circuit_a, QuantumCircuit):
        raise QuantestPyError(
            "Type of qiskit_circuit_a must be an instance of "
            "qiskit.QuantumCircuit class."
        )

    if test_circuit_a is not None \
            and not isinstance(test_circuit_a, TestCircuit):
        raise QuantestPyError(
            "Type of test_circuit_a must be an instance of "
            "quantestpy.TestCircuit class."
        )

    # Check inputs for circuit B
    if qasm_b is None and qiskit_circuit_b is None and test_circuit_b is None:
        raise QuantestPyError(
            "Missing information for circuit B. "
            "One of the following must be given: "
            "qasm_b, qiskit_circuit_b and test_circuit_b."
        )

    if (qasm_b is not None and qiskit_circuit_b is not None) \
            or (qasm_b is not None and test_circuit_b is not None) \
            or (qiskit_circuit_b is not None and test_circuit_b is not None):
        raise QuantestPyError(
            "Too much information for circuit B. "
            "Only one of the following should be given: "
            "qasm_b, qiskit_circuit_b and test_circuit_b."
        )

    if qasm_b is not None and not isinstance(qasm_b, str):
        raise QuantestPyError(
            "Type of qasm_b must be str."
        )

    if qiskit_circuit_b is not None \
            and not isinstance(qiskit_circuit_b, QuantumCircuit):
        raise QuantestPyError(
            "Type of qiskit_circuit_b must be an instance of "
            "qiskit.QuantumCircuit class."
        )

    if test_circuit_b is not None \
            and not isinstance(test_circuit_b, TestCircuit):
        raise QuantestPyError(
            "Type of test_circuit_b must be an instance of "
            "quantestpy.TestCircuit class."
        )

    if matrix_norm_type is not None and matrix_norm_type not in \
        ["operator_norm_1", "operator_norm_2",
         "operator_norm_inf", "Frobenius_norm", "max_norm"]:
        raise QuantestPyError(
            "Invalid value for matrix_norm_type. "
            "One of the following should be chosen: "
            "'operator_norm_1', 'operator_norm_2', 'operator_norm_inf', "
            "'Frobenius_norm' and 'max_norm'."
        )

    if not isinstance(tolerance_for_matrix_norm_value, float) \
            and tolerance_for_matrix_norm_value is not None:
        raise QuantestPyError(
            "Type of tolerance_for_matrix_norm_value must be float."
        )

    # cvt. to test_circuit_a
    if qasm_a is not None:
        test_circuit_a = _cvt_openqasm_to_test_circuit(qasm_a)

    elif qiskit_circuit_a is not None:
        test_circuit_a = _cvt_qiskit_to_test_circuit(qiskit_circuit_a)

    # cvt. to test_circuit_b
    if qasm_b is not None:
        test_circuit_b = _cvt_openqasm_to_test_circuit(qasm_b)

    elif qiskit_circuit_b is not None:
        test_circuit_b = _cvt_qiskit_to_test_circuit(qiskit_circuit_b)

    whole_gates_a = test_circuit_a._get_whole_gates()
    whole_gates_b = test_circuit_b._get_whole_gates()

    if matrix_norm_type is None:
        # assert equal exact or equal up to a global phase
        operator.assert_equal(
            whole_gates_a,
            whole_gates_b,
            number_of_decimal_places,
            up_to_global_phase,
            msg)

    else:
        # assert check matrix norm as a distance
        matrix_norm_value = _get_matrix_norm(
            whole_gates_a,
            whole_gates_b,
            matrix_norm_type,
            up_to_global_phase
        )

        if tolerance_for_matrix_norm_value is None:
            tolerance_for_matrix_norm_value = 0.

        if matrix_norm_value > tolerance_for_matrix_norm_value:

            error_msg = "matrix norm value " \
                + format(matrix_norm_value, ".15g") \
                + " is larger than the tolerance " \
                + format(tolerance_for_matrix_norm_value, ".15g") + "."
            msg = ut_test_case._formatMessage(msg, error_msg)
            raise QuantestPyAssertionError(msg)
