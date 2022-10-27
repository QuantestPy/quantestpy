import copy
import unittest

import numpy as np

from quantestpy import FastTestCircuit
from quantestpy.exceptions import QuantestPyAssertionError

ut_test_case = unittest.TestCase()


def assert_equal_unary_iteration(
        circuit: FastTestCircuit,
        control_qubits: list,
        control_values: list,
        selection_register_qubits: list,
        system_register_qubits: list,
        ancilla_register_qubits: list = [],
        verbose: bool = False,
        msg=None):

    user_ftc = copy.deepcopy(circuit)
    size_selection_register = len(selection_register_qubits)
    size_system_register = len(system_register_qubits)

    # cvt all opearations to X
    for i, gate in enumerate(user_ftc._gates):
        if len(gate["target_qubit"]) == 1 and \
                gate["target_qubit"][0] in system_register_qubits:
            user_ftc._gates[i]["name"] = "x"

    # execute ftc for all computational bases of selection_register
    for l_ in range(size_system_register):
        l_binary_rep = ("0" * size_selection_register +
                        bin(l_)[2:])[-size_selection_register:]

        # set all control qubits to active in user circuit
        user_ftc.set_qubit_value(
            qubit_id=control_qubits,
            qubit_value=control_values
        )
        # initialize all system register qubits to 0 in user circuit
        user_ftc.set_qubit_value(
            qubit_id=system_register_qubits,
            qubit_value=[0] * size_system_register
        )
        # initialize all the ancilla qubits to 0 in user circuit
        user_ftc.set_qubit_value(
            qubit_id=ancilla_register_qubits,
            qubit_value=[0] * len(ancilla_register_qubits)
        )
        # initialize the selection register to l_binary_rep
        user_ftc.set_qubit_value(
            qubit_id=selection_register_qubits,
            qubit_value=[int(i) for i in l_binary_rep]
        )
        user_ftc.execute_all_gates()

        if verbose:
            print(user_ftc._qubit_value[system_register_qubits])

        expected_qubit_value_of_system_register_qubits = \
            np.array([0]*size_system_register)
        expected_qubit_value_of_system_register_qubits[l_] = 1

        # check assert equal
        if not np.all(expected_qubit_value_of_system_register_qubits
                      == user_ftc._qubit_value[system_register_qubits]):
            error_msg = "output from system register is not correct when " \
                + f"input to selection register is {l_binary_rep}."
            msg = ut_test_case._formatMessage(msg, error_msg)
            raise QuantestPyAssertionError(msg)

        # check all ancillas are back to 0
        if not np.all(user_ftc._qubit_value[ancilla_register_qubits] == 0):
            error_msg = "ancilla qubit(s) are not back to 0 when " \
                + f"input to selection register is {l_binary_rep}."
            msg = ut_test_case._formatMessage(msg, error_msg)
            raise QuantestPyAssertionError(msg)
