import unittest
import numpy as np
from typing import Union
import itertools
import traceback
import re

from quantestpy import operator
from quantestpy import TestCircuit
from quantestpy.exceptions import QuantestPyError, QuantestPyAssertionError
from quantestpy.test_circuit import cvt_openqasm_to_test_circuit

ut_test_case = unittest.TestCase()


def assert_equal_to_operator(
        operator_: Union[np.ndarray, np.matrix],
        qasm: str = None,
        test_circuit: TestCircuit = None,
        from_right_to_left_for_qubit_ids: bool = False,
        number_of_decimal_places: int = 5,
        check_including_global_phase: bool = True,
        msg=None) -> None:

    #
    if qasm is None and test_circuit is None:
        raise QuantestPyError(
            "Missing qasm or test circuit."
        )

    if qasm is not None and test_circuit is not None:
        raise QuantestPyError(
            "Qasm and test circuit must not both be given."
        )

    if qasm is not None:
        test_circuit = cvt_openqasm_to_test_circuit(qasm)
        raise QuantestPyError(
            "Loading qasm is not yet implemented."
        )

    test_circuit._from_right_to_left_for_qubit_ids = \
        from_right_to_left_for_qubit_ids

    operator_from_test_circuit = test_circuit._get_whole_gates()

    operator.assert_equal(
        operator_from_test_circuit,
        operator_,
        number_of_decimal_places,
        check_including_global_phase,
        msg)


def assert_is_zero(qasm: str = None,
                   test_circuit: TestCircuit = None,
                   qubits: list = None,
                   number_of_decimal_places: int = 5,
                   msg=None) -> None:

    # Memo220805JN: the following input checker may be common for the other
    # functions in this module, thus can be one function.
    if qasm is None and test_circuit is None:
        raise QuantestPyError(
            "Missing qasm or test circuit."
        )

    if qasm is not None and test_circuit is not None:
        raise QuantestPyError(
            "Qasm and test circuit must not both be given."
        )

    if qasm is not None:
        test_circuit = cvt_openqasm_to_test_circuit(qasm)
        raise QuantestPyError(
            "Loading qasm is not yet implemented."
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
            clipped_state_vec = np.round(
                clipped_state_vec, decimals=number_of_decimal_places)

            if not np.all(clipped_state_vec == 0.):
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
                           test_circuit: TestCircuit = None,
                           number_of_decimal_places: int = 5,
                           msg=None) -> None:

    if qasm is None and test_circuit is None:
        raise QuantestPyError(
            "Missing qasm or test circuit."
        )

    if qasm is not None and test_circuit is not None:
        raise QuantestPyError(
            "Qasm and test circuit must not both be given."
        )

    if qasm is not None:
        test_circuit = cvt_openqasm_to_test_circuit(qasm)
        raise QuantestPyError(
            "Loading qasm is not yet implemented."
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
        x_gate = {'name': 'x',
                  'target_qubit': [qubit],
                  'control_qubit': [],
                  'control_value': []}
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
                           number_of_decimal_places=number_of_decimal_places)

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
