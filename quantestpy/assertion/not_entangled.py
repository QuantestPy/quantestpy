import unittest

import numpy as np

from quantestpy.converter.converter_to_quantestpy_circuit import \
    cvt_input_circuit_to_quantestpy_circuit
from quantestpy.exceptions import QuantestPyAssertionError, QuantestPyError
from quantestpy.simulator.state_vector_circuit import \
    cvt_quantestpy_circuit_to_state_vector_circuit

ut_test_case = unittest.TestCase()


def assert_not_entangled(circuit,
                         qubits: list = [],
                         atol: float = 1e-12,
                         msg=None):

    quantestpy_circuit = cvt_input_circuit_to_quantestpy_circuit(circuit)
    num_qubit = quantestpy_circuit.num_qubit

    if not isinstance(qubits, list):
        raise QuantestPyError("qubits must be a list of integer(s).")
    for qubit in qubits:
        if not isinstance(qubit, int):
            raise QuantestPyError("Elements in qubits must be integer.")
        if qubit > num_qubit - 1 or qubit < 0:
            raise QuantestPyError("qubits out of range.")

    state_vector_circuit = cvt_quantestpy_circuit_to_state_vector_circuit(
        quantestpy_circuit
    )
    state_vec = state_vector_circuit._get_state_vector()

    # all qubit if not given by users
    if len(qubits) == 0:
        qubits = state_vector_circuit.qubit_indices

    # Extract the computational bases with non-zero wave functions
    non_zero_basis_list = []
    for decimal in range(2**num_qubit):
        bitstring = ("0" * num_qubit + bin(decimal)[2:])[-num_qubit:]
        wave_func = state_vec[decimal]
        if np.abs(wave_func) > atol:
            non_zero_basis_list.append(bitstring)

    # Search for entangled pairs
    qubit_to_entangled_qubits = {qubit: [] for qubit in qubits}
    for qubit_id_0 in qubits:
        for qubit_id_1 in range(num_qubit):
            if qubit_id_0 == qubit_id_1:
                continue

            val_pair_list = []
            for basis in non_zero_basis_list:
                qubit_val_0 = basis[qubit_id_0]
                qubit_val_1 = basis[qubit_id_1]
                val_pair = qubit_val_0 + qubit_val_1
                val_pair_list.append(val_pair)

            val_pair_uniq_list = set(val_pair_list)
            if len(val_pair_uniq_list) == 2:
                val_pair_0, val_pair_1 = val_pair_uniq_list
                if val_pair_0[0] != val_pair_1[0] \
                        and val_pair_0[1] != val_pair_1[1]:
                    qubit_to_entangled_qubits[qubit_id_0].append(qubit_id_1)

    # Construct error messages
    err_msg_list = []
    for qubit, entangled_qubit_list in qubit_to_entangled_qubits.items():
        if len(entangled_qubit_list) > 0:
            err_msg = f"qubit {qubit} is entangled with qubit(s) " \
                + f"{entangled_qubit_list}."
            err_msg_list.append(err_msg)

    if len(err_msg_list) > 0:
        err_msg = "\n".join(err_msg_list)
        msg = ut_test_case._formatMessage(msg, err_msg)
        raise QuantestPyAssertionError(msg)
