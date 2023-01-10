import unittest

import numpy as np

from quantestpy.converter.converter_to_quantestpy_circuit import \
    cvt_input_circuit_to_quantestpy_circuit
from quantestpy.exceptions import QuantestPyAssertionError, QuantestPyError
from quantestpy.simulator.pauli_circuit import (
    PauliCircuit, cvt_quantestpy_circuit_to_pauli_circuit)

ut_test_case = unittest.TestCase()


def _get_qubit_idx_to_qubit_val_for_given_val_in_ctrl_reg(
        val_in_ctrl_reg: str,
        pc: PauliCircuit,
        ctrl_reg: list,
        ancilla_reg: list) -> dict:

    # init ancilla reg to 0
    pc.set_qubit_value(ancilla_reg, [0] * len(ancilla_reg))
    # init ctrl reg to val_in_ctrl_reg
    pc.set_qubit_value(ctrl_reg, [int(i) for i in val_in_ctrl_reg])

    # get ctrl vals for all ops on syst reg
    qubit_idx_to_qubit_val = {idx: [] for idx in ctrl_reg + ancilla_reg}
    for i, gate in enumerate(pc._gates):

        qubit_idx = gate["control_qubit"]
        qubit_val = pc._qubit_value[qubit_idx]

        for j, idx in enumerate(qubit_idx):
            if idx in qubit_idx_to_qubit_val.keys():
                qubit_idx_to_qubit_val[idx].append(qubit_val[j])

        pc._execute_i_th_gate(i)

    return qubit_idx_to_qubit_val


def assert_get_ctrl_val(
        circuit,
        ctrl_reg: list,
        ancilla_reg: list = [],
        check_ancilla_is_uncomputed: bool = False,
        print_out_result: bool = True) -> dict:

    quantestpy_circuit = cvt_input_circuit_to_quantestpy_circuit(circuit)
    pc = cvt_quantestpy_circuit_to_pauli_circuit(quantestpy_circuit)

    # check inputs
    pc._assert_is_correct_reg(ctrl_reg)
    pc._assert_is_correct_reg(ancilla_reg)
    if not isinstance(check_ancilla_is_uncomputed, bool):
        raise QuantestPyError("check_assert_is_uncomputed must be bool type.")
    if not isinstance(print_out_result, bool):
        raise QuantestPyError("print_out_result must be bool type.")

    len_ctrl_reg = len(ctrl_reg)
    idx_to_val_in_ctrl_reg_to_val = \
        {idx: dict() for idx in ctrl_reg + ancilla_reg}

    for dec_val_in_ctrl_reg in range(2**len_ctrl_reg):

        bin_val_in_ctrl_reg = \
            ("0" * len_ctrl_reg + bin(dec_val_in_ctrl_reg)[2:])[-len_ctrl_reg:]

        qubit_idx_to_qubit_val = \
            _get_qubit_idx_to_qubit_val_for_given_val_in_ctrl_reg(
                bin_val_in_ctrl_reg,
                pc,
                ctrl_reg,
                ancilla_reg
            )

        if check_ancilla_is_uncomputed:
            if not np.all(pc._qubit_value[ancilla_reg] == 0):
                err_msg = "ancilla reg is not back to 0 by uncomputation " \
                    + f"when val in ctrl reg is {bin_val_in_ctrl_reg}."
                raise QuantestPyAssertionError(err_msg)

        if print_out_result:
            print(f"val in ctrl reg: {bin_val_in_ctrl_reg},",
                  f"qubit idx to qubit val: {qubit_idx_to_qubit_val}")

        for idx, val in qubit_idx_to_qubit_val.items():
            idx_to_val_in_ctrl_reg_to_val[idx][bin_val_in_ctrl_reg] = val

    return idx_to_val_in_ctrl_reg_to_val
