import itertools
import re
import traceback
import unittest
from typing import Union

from quantestpy import QuantestPyCircuit
from quantestpy.assertion.assert_qubit_reset_to_zero_state import \
    assert_qubit_reset_to_zero_state
from quantestpy.converter.converter_to_quantestpy_circuit import \
    cvt_input_circuit_to_quantestpy_circuit
from quantestpy.exceptions import QuantestPyAssertionError, QuantestPyError

ut_test_case = unittest.TestCase()


def assert_ancilla_reset(circuit: Union[QuantestPyCircuit, str],
                         ancilla_qubits: list,
                         atol: float = 1e-8,
                         msg=None) -> None:

    if not isinstance(ancilla_qubits, list):
        raise QuantestPyError(
            "ancilla_qubits must be a list of integer(s) as qubit's ID(s)."
        )

    quantestpy_circuit = cvt_input_circuit_to_quantestpy_circuit(circuit)

    num_qubit = quantestpy_circuit.num_qubit

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

        # add x gate(s) in quantestpy_circuit
        for system_qubit in comb_of_sys_qubits:
            _add_x_gate_in_front(quantestpy_circuit._gates, system_qubit)

        # assertion using assert_is_zero
        try:
            assert_qubit_reset_to_zero_state(circuit=quantestpy_circuit,
                                             qubits=ancilla_qubits,
                                             atol=atol)

        except QuantestPyAssertionError as e:
            t = traceback.format_exception_only(type(e), e)[0]
            error_msgs_from_assert_is_zero.append(t)

        # remove x gate(s) from quantestpy_circuit,
        # i.e. reset quantestpy_circuit.
        for _ in comb_of_sys_qubits:
            del quantestpy_circuit._gates[0]

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
