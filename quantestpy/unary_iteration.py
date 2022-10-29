import copy
import unittest

import numpy as np

from quantestpy import FastTestCircuit
from quantestpy.exceptions import QuantestPyAssertionError

ut_test_case = unittest.TestCase()


def assert_equal_single_operation(
        circuit: FastTestCircuit,
        selection_register_qubits: list,
        system_register_qubits: list,
        control_qubits: list = [],
        control_values: list = [],
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
            print(l_, user_ftc._qubit_value[system_register_qubits])

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


def assert_equal_ranged_operation(
        circuit: FastTestCircuit,
        selection_register_qubits: list,
        system_register_qubits: list,
        accumulator_qubit: list,
        control_qubits: list = [],
        control_values: list = [],
        ancilla_register_qubits: list = [],
        verbose: bool = False,
        msg=None):

    user_ftc = copy.deepcopy(circuit)
    size_selection_register = len(selection_register_qubits)
    size_system_register = len(system_register_qubits)

    # cvt all opearations to X
    for i, gate in enumerate(user_ftc._gates):
        if len(gate["target_qubit"]) == 1 and \
            gate["target_qubit"][0] in system_register_qubits and \
                gate["control_qubit"][0] in accumulator_qubit:
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
        # initialize the accumulator to 0 in user circuit
        user_ftc.set_qubit_value(
            qubit_id=accumulator_qubit,
            qubit_value=[0]
        )
        # initialize the selection register to l_binary_rep
        user_ftc.set_qubit_value(
            qubit_id=selection_register_qubits,
            qubit_value=[int(i) for i in l_binary_rep]
        )
        user_ftc.execute_all_gates()

        if verbose:
            print(l_, user_ftc._qubit_value[system_register_qubits])

        expected_qubit_value_of_system_register_qubits = \
            np.array([0]*size_system_register)
        expected_qubit_value_of_system_register_qubits[:l_] = 1

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

        # check accumulator is back to 0
        if not np.all(user_ftc._qubit_value[accumulator_qubit] == 0):
            error_msg = "accumulator is not back to 0 when " \
                + f"input to selection register is {l_binary_rep}."
            msg = ut_test_case._formatMessage(msg, error_msg)
            raise QuantestPyAssertionError(msg)


def assert_equal_Majorana_operation(
        circuit: FastTestCircuit,
        selection_register_qubits: list,
        system_register_qubits: list,
        accumulator_qubit: list,
        control_qubits: list = [],
        control_values: list = [],
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
        # initialize the accumulator to 0 in user circuit
        user_ftc.set_qubit_value(
            qubit_id=accumulator_qubit,
            qubit_value=[0]
        )
        # initialize the selection register to l_binary_rep
        user_ftc.set_qubit_value(
            qubit_id=selection_register_qubits,
            qubit_value=[int(i) for i in l_binary_rep]
        )
        user_ftc.execute_all_gates()

        if verbose:
            print(l_, user_ftc._qubit_value[system_register_qubits])

        expected_qubit_value_of_system_register_qubits = \
            np.array([0]*size_system_register)
        expected_qubit_value_of_system_register_qubits[:l_+1] = 1

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

        # check accumulator is back to 0
        if not np.all(user_ftc._qubit_value[accumulator_qubit] == 0):
            error_msg = "accumulator is not back to 0 when " \
                + f"input to selection register is {l_binary_rep}."
            msg = ut_test_case._formatMessage(msg, error_msg)
            raise QuantestPyAssertionError(msg)


def assert_check_control_values_for_operations_on_system_register(
        circuit: FastTestCircuit,
        selection_register_qubits: list,
        system_register_qubits: list,
        accumulator_qubits: list = [],
        control_qubits: list = [],
        control_values: list = [],
        ancilla_register_qubits: list = [],
        loop_over_all_selection_register_inputs: bool = True):

    user_ftc = copy.deepcopy(circuit)
    size_selection_register = len(selection_register_qubits)

    selection_register_bound = 2**size_selection_register if \
        loop_over_all_selection_register_inputs else \
        len(system_register_qubits)

    for l_ in range(selection_register_bound):
        l_binary_rep = ("0" * size_selection_register +
                        bin(l_)[2:])[-size_selection_register:]

        # set all control qubits to active in user circuit
        user_ftc.set_qubit_value(
            qubit_id=control_qubits,
            qubit_value=control_values
        )
        # initialize all the ancilla qubits to 0 in user circuit
        user_ftc.set_qubit_value(
            qubit_id=ancilla_register_qubits,
            qubit_value=[0] * len(ancilla_register_qubits)
        )
        # initialize the accumulator to 0 in user circuit
        user_ftc.set_qubit_value(
            qubit_id=accumulator_qubits,
            qubit_value=[0] * len(accumulator_qubits)
        )
        # initialize the selection register to l_binary_rep
        user_ftc.set_qubit_value(
            qubit_id=selection_register_qubits,
            qubit_value=[int(i) for i in l_binary_rep]
        )

        control_qubit_values = []
        for i, gate in enumerate(user_ftc._gates):

            if np.all([qubit in system_register_qubits for qubit
                       in gate["target_qubit"]]):
                control_qubit = gate["control_qubit"]
                control_qubit_values.append(
                    user_ftc._qubit_value[control_qubit].tolist())

            else:
                user_ftc.execute_one_gate(i)

        print(f"l_binary rep.: {l_binary_rep},",
              f"control qubit values: {control_qubit_values}")


def assert_equal_control_values_for_operations_on_system_register(
        circuit: FastTestCircuit,
        expected_selection_register_value_to_control_value: dict,
        selection_register_qubits: list,
        system_register_qubits: list,
        accumulator_qubits: list = [],
        control_qubits: list = [],
        control_values: list = [],
        ancilla_register_qubits: list = [],
        msg=None):

    user_ftc = copy.deepcopy(circuit)

    for l_binary_rep, expected_control_qubit_values in \
            expected_selection_register_value_to_control_value.items():

        # set all control qubits to active in user circuit
        user_ftc.set_qubit_value(
            qubit_id=control_qubits,
            qubit_value=control_values
        )
        # initialize all the ancilla qubits to 0 in user circuit
        user_ftc.set_qubit_value(
            qubit_id=ancilla_register_qubits,
            qubit_value=[0] * len(ancilla_register_qubits)
        )
        # initialize the accumulator to 0 in user circuit
        user_ftc.set_qubit_value(
            qubit_id=accumulator_qubits,
            qubit_value=[0] * len(accumulator_qubits)
        )
        # initialize the selection register to l_binary_rep
        user_ftc.set_qubit_value(
            qubit_id=selection_register_qubits,
            qubit_value=[int(i) for i in l_binary_rep]
        )

        control_qubit_values = []
        for i, gate in enumerate(user_ftc._gates):

            if np.all([qubit in system_register_qubits for qubit
                       in gate["target_qubit"]]):
                control_qubit = gate["control_qubit"]
                control_qubit_values.append(
                    user_ftc._qubit_value[control_qubit].tolist())

            else:
                user_ftc.execute_one_gate(i)

        if len(control_qubit_values) != len(expected_control_qubit_values):
            error_msg = "The number of operations is not as expected " \
                + f"when input to selection register is {l_binary_rep}: \n" \
                + f"expect: {len(expected_control_qubit_values)} \n" \
                + f"actual: {len(control_qubit_values)}"
            msg = ut_test_case._formatMessage(msg, error_msg)
            raise QuantestPyAssertionError(msg)

        if not np.allclose(control_qubit_values,
                           expected_control_qubit_values):
            error_msg = "control qubit value(s) are not equal to your " \
                + "expectation when input to selection register is " \
                + f"{l_binary_rep}: \n" \
                + f"expect: {expected_control_qubit_values} \n" \
                + f"actual: {control_qubit_values}"
            msg = ut_test_case._formatMessage(msg, error_msg)
            raise QuantestPyAssertionError(msg)

        # check all ancillas are back to 0
        if not np.all(user_ftc._qubit_value[ancilla_register_qubits] == 0):
            error_msg = "ancilla qubit(s) are not back to 0 when " \
                + f"input to selection register is {l_binary_rep}."
            msg = ut_test_case._formatMessage(msg, error_msg)
            raise QuantestPyAssertionError(msg)

        # check accumulator is back to 0
        if not np.all(user_ftc._qubit_value[accumulator_qubits] == 0):
            error_msg = "accumulator is not back to 0 when " \
                + f"input to selection register is {l_binary_rep}."
            msg = ut_test_case._formatMessage(msg, error_msg)
            raise QuantestPyAssertionError(msg)
