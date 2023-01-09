import copy
import unittest

import numpy as np

from quantestpy import PauliCircuit
from quantestpy.exceptions import QuantestPyAssertionError, QuantestPyError

ut_test_case = unittest.TestCase()


def _get_tgt_qubit_idx_to_qubit_val_for_given_val_in_ctrl_reg(
        val_in_ctrl_reg: str,
        pc: PauliCircuit,
        tgt_reg: list,
        ctrl_reg: list,
        ancilla_reg: list) -> dict:

    # init ancilla reg to 0
    pc.set_qubit_value(ancilla_reg, [0] * len(ancilla_reg))
    # init ctrl reg to val_in_ctrl_reg
    pc.set_qubit_value(ctrl_reg, [int(i) for i in val_in_ctrl_reg])
    # init tgt reg to 0
    pc.set_qubit_value(tgt_reg, [0] * len(tgt_reg))

    # get tgt vals for all ops on tgt reg
    qubit_idx_to_qubit_val = {idx: [0] for idx in tgt_reg}

    for i, gate in enumerate(pc._gates):
        pc._execute_i_th_gate(i)

        qubit_idx = gate["target_qubit"]
        qubit_val = pc._qubit_value[qubit_idx]

        for j, idx in enumerate(qubit_idx):
            if idx in tgt_reg:
                if idx in qubit_idx_to_qubit_val.keys():
                    qubit_idx_to_qubit_val[idx].append(qubit_val[j])

    return qubit_idx_to_qubit_val


def assert_get_tgt_val(
        circuit: PauliCircuit,
        tgt_reg: list,
        ctrl_reg: list,
        ancilla_reg: list = [],
        check_ancilla_is_uncomputed: bool = False,
        print_out_result: bool = True) -> dict:

    # check inputs
    PauliCircuit._assert_is_pauli_circuit(circuit)
    pc = copy.deepcopy(circuit)
    pc._assert_is_correct_reg(ctrl_reg)
    pc._assert_is_correct_reg(ancilla_reg)
    pc._assert_is_correct_reg(tgt_reg)
    if not isinstance(check_ancilla_is_uncomputed, bool):
        raise QuantestPyError("check_assert_is_uncomputed must be bool type.")
    if not isinstance(print_out_result, bool):
        raise QuantestPyError("print_out_result must be bool type.")

    len_ctrl_reg = len(ctrl_reg)
    idx_to_val_in_tgt_reg_to_val = {idx: dict() for idx in tgt_reg}

    for dec_val_in_ctrl_reg in range(2**len_ctrl_reg):

        bin_val_in_ctrl_reg = \
            ("0" * len_ctrl_reg + bin(dec_val_in_ctrl_reg)[2:])[-len_ctrl_reg:]

        qubit_idx_to_qubit_val = \
            _get_tgt_qubit_idx_to_qubit_val_for_given_val_in_ctrl_reg(
                bin_val_in_ctrl_reg,
                pc,
                tgt_reg,
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
            idx_to_val_in_tgt_reg_to_val[idx][bin_val_in_ctrl_reg] = val

    return idx_to_val_in_tgt_reg_to_val
