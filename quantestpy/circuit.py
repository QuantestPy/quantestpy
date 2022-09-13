import unittest
import numpy as np
from typing import Union
import itertools
import traceback
import re

from quantestpy import operator
from quantestpy import TestCircuit
from quantestpy.exceptions import QuantestPyError, QuantestPyAssertionError
from quantestpy.converter import _cvt_qiskit_to_test_circuit
from quantestpy.converter import _cvt_openqasm_to_test_circuit
from quantestpy.converter import _is_instance_of_qiskit_quantumcircuit
from quantestpy.state_vector import _remove_global_phase_from_two_vectors

ut_test_case = unittest.TestCase()


def assert_equal_to_operator(
        circuit: Union[TestCircuit, str],
        operator_: Union[np.ndarray, np.matrix],
        from_right_to_left_for_qubit_ids: bool = False,
        rtol: float = 0.,
        atol: float = 1e-8,
        up_to_global_phase: bool = False,
        msg=None) -> None:

    # test_circuit
    if isinstance(circuit, TestCircuit):
        test_circuit = circuit

    # qasm
    elif isinstance(circuit, str):
        test_circuit = _cvt_openqasm_to_test_circuit(circuit)

    # qiskit.QuantumCircuit()
    elif _is_instance_of_qiskit_quantumcircuit(circuit):
        test_circuit = _cvt_qiskit_to_test_circuit(circuit)

    else:
        raise QuantestPyError(
            "Input circuit must be one of the following: "
            "qasm, qiskit.QuantumCircuit and TestCircuit."
        )

    test_circuit._from_right_to_left_for_qubit_ids = \
        from_right_to_left_for_qubit_ids

    operator_from_test_circuit = test_circuit._get_whole_gates()

    operator.assert_equal(
        operator_from_test_circuit,
        operator_,
        rtol,
        atol,
        up_to_global_phase,
        msg)


def assert_is_zero(circuit: Union[TestCircuit, str],
                   qubits: list = None,
                   atol: float = 1e-8,
                   msg=None) -> None:

    # test_circuit
    if isinstance(circuit, TestCircuit):
        test_circuit = circuit

    # qasm
    elif isinstance(circuit, str):
        test_circuit = _cvt_openqasm_to_test_circuit(circuit)

    # qiskit.QuantumCircuit()
    elif _is_instance_of_qiskit_quantumcircuit(circuit):
        test_circuit = _cvt_qiskit_to_test_circuit(circuit)

    else:
        raise QuantestPyError(
            "Input circuit must be one of the following: "
            "qasm, qiskit.QuantumCircuit and TestCircuit."
        )

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
            clipped_state_vec = np.abs(clipped_state_vec)

            if not np.all(clipped_state_vec <= atol):
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


def assert_ancilla_is_zero(circuit: Union[TestCircuit, str],
                           ancilla_qubits: list,
                           atol: float = 1e-8,
                           msg=None) -> None:

    # test_circuit
    if isinstance(circuit, TestCircuit):
        test_circuit = circuit

    # qasm
    elif isinstance(circuit, str):
        test_circuit = _cvt_openqasm_to_test_circuit(circuit)

    # qiskit.QuantumCircuit()
    elif _is_instance_of_qiskit_quantumcircuit(circuit):
        test_circuit = _cvt_qiskit_to_test_circuit(circuit)

    else:
        raise QuantestPyError(
            "Input circuit must be one of the following: "
            "qasm, qiskit.QuantumCircuit and TestCircuit."
        )

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
            assert_is_zero(circuit=test_circuit,
                           qubits=ancilla_qubits,
                           atol=atol)

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
        circuit_a: Union[TestCircuit, str],
        circuit_b: Union[TestCircuit, str],
        rtol: float = 0.,
        atol: float = 1e-8,
        up_to_global_phase: bool = False,
        matrix_norm_type: Union[str, None] = None,
        msg: Union[str, None] = None):

    # Check inputs for circuit A
    # test_circuit
    if isinstance(circuit_a, TestCircuit):
        test_circuit_a = circuit_a

    # qasm
    elif isinstance(circuit_a, str):
        test_circuit_a = _cvt_openqasm_to_test_circuit(circuit_a)

    # qiskit.QuantumCircuit()
    elif _is_instance_of_qiskit_quantumcircuit(circuit_a):
        test_circuit_a = _cvt_qiskit_to_test_circuit(circuit_a)

    else:
        raise QuantestPyError(
            "circuit_a must be one of the following: "
            "qasm, qiskit.QuantumCircuit and TestCircuit."
        )

    # Check inputs for circuit B
    # test_circuit
    if isinstance(circuit_b, TestCircuit):
        test_circuit_b = circuit_b

    # qasm
    elif isinstance(circuit_b, str):
        test_circuit_b = _cvt_openqasm_to_test_circuit(circuit_b)

    # qiskit.QuantumCircuit()
    elif _is_instance_of_qiskit_quantumcircuit(circuit_b):
        test_circuit_b = _cvt_qiskit_to_test_circuit(circuit_b)

    else:
        raise QuantestPyError(
            "circuit_b must be one of the following: "
            "qasm, qiskit.QuantumCircuit and TestCircuit."
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

    if not isinstance(atol, float):
        raise QuantestPyError(
            "Type of atol must be float."
        )

    if not isinstance(rtol, float):
        raise QuantestPyError(
            "Type of rtol must be float."
        )

    whole_gates_a = test_circuit_a._get_whole_gates()
    whole_gates_b = test_circuit_b._get_whole_gates()

    if matrix_norm_type is None:
        # assert equal exact or equal up to a global phase
        operator.assert_equal(
            whole_gates_a,
            whole_gates_b,
            rtol,
            atol,
            up_to_global_phase,
            msg)

    else:
        # assert check matrix norm as a distance
        matrix_norm_a_minus_b = _get_matrix_norm(
            whole_gates_a,
            whole_gates_b,
            matrix_norm_type,
            up_to_global_phase
        )

        if rtol != 0.:
            matrix_norm_b = _get_matrix_norm(
                whole_gates_b,
                np.zeros_like(whole_gates_b),
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
