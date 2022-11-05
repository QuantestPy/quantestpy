import copy
import unittest

import numpy as np

from quantestpy import FastTestCircuit
from quantestpy.exceptions import QuantestPyAssertionError, QuantestPyError

ut_test_case = unittest.TestCase()


def _get_ctrl_val_of_all_ops_on_syst_reg_for_given_val_in_select_reg(
        val_in_select_reg: str,
        ftc: FastTestCircuit,
        select_reg: list,
        system_reg: list,
        ancilla_reg: list) -> list:

    # init ancilla reg to 0
    ftc.set_qubit_value(ancilla_reg, [0] * len(ancilla_reg))
    # init select reg to val_in_select_reg
    ftc.set_qubit_value(select_reg, [int(i) for i in val_in_select_reg])

    # get ctrl vals for all ops on syst reg
    ctrl_val_of_all_ops = []
    for i, gate in enumerate(ftc._gates):

        if np.all([idx in system_reg for idx in gate["target_qubit"]]):
            ctrl_qubit_for_one_op = gate["control_qubit"]
            ctrl_val_of_all_ops.append(
                ftc._qubit_value[ctrl_qubit_for_one_op].tolist()
            )

        else:
            ftc._execute_i_th_gate(i)

    return ctrl_val_of_all_ops


def _get_qubit_idx_to_ctrl_val_for_given_val_in_select_reg(
        val_in_select_reg: str,
        ftc: FastTestCircuit,
        select_reg: list,
        ancilla_reg: list) -> dict:

    # init ancilla reg to 0
    ftc.set_qubit_value(ancilla_reg, [0] * len(ancilla_reg))
    # init select reg to val_in_select_reg
    ftc.set_qubit_value(select_reg, [int(i) for i in val_in_select_reg])

    # get ctrl vals for all ops on syst reg
    qubit_idx_to_ctrl_val = {idx: [] for idx in select_reg + ancilla_reg}
    for i, gate in enumerate(ftc._gates):

        ctrl_qubit_idx_for_one_op = gate["control_qubit"]
        ctrl_qubit_val_for_one_op = \
            ftc._qubit_value[ctrl_qubit_idx_for_one_op].tolist()

        for j, ctrl_qubit_idx in enumerate(ctrl_qubit_idx_for_one_op):
            if ctrl_qubit_idx in qubit_idx_to_ctrl_val.keys():
                qubit_idx_to_ctrl_val[ctrl_qubit_idx].append(
                    ctrl_qubit_val_for_one_op[j])

        ftc._execute_i_th_gate(i)

    return qubit_idx_to_ctrl_val


def assert_check_ctrl_val_of_all_ops_on_syst_reg(
        circuit: FastTestCircuit,
        select_reg: list,
        system_reg: list,
        ancilla_reg: list = []):

    # check inputs
    FastTestCircuit._assert_is_fast_test_circuit(circuit, "Input circuit")
    ftc = copy.deepcopy(circuit)
    ftc._assert_is_correct_reg(select_reg, "select_reg")
    ftc._assert_is_correct_reg(system_reg, "system_reg")
    ftc._assert_is_correct_reg(ancilla_reg, "ancilla_reg")

    len_select_reg = len(select_reg)

    for dec_val_in_select_reg in range(2**len_select_reg):

        bin_val_in_select_reg = \
            ("0" * len_select_reg + bin(dec_val_in_select_reg)[2:])[
                -len_select_reg:]

        ctrl_val_of_all_ops = \
            _get_ctrl_val_of_all_ops_on_syst_reg_for_given_val_in_select_reg(
                bin_val_in_select_reg,
                ftc,
                select_reg,
                system_reg,
                ancilla_reg
            )

        print(f"val in select reg: {bin_val_in_select_reg},",
              f"ctrl val of all ops: {ctrl_val_of_all_ops}")


def assert_equal_ctrl_val_of_all_ops_on_syst_reg(
        circuit: FastTestCircuit,
        select_reg: list,
        system_reg: list,
        expected_val_in_select_reg_to_ctrl_val: dict,
        ancilla_reg: list = [],
        assert_is_ancilla_uncomputated: bool = True,
        msg=None):

    # check inputs
    FastTestCircuit._assert_is_fast_test_circuit(circuit, "Input circuit")
    ftc = copy.deepcopy(circuit)
    ftc._assert_is_correct_reg(select_reg, "select_reg")
    ftc._assert_is_correct_reg(system_reg, "system_reg")
    ftc._assert_is_correct_reg(ancilla_reg, "ancilla_reg")
    if not isinstance(expected_val_in_select_reg_to_ctrl_val, dict):
        raise QuantestPyError(
            "expected_val_in_select_reg_to_ctrl_val must be dict type."
        )

    for bin_val_in_select_reg, expected_ctrl_val in \
            expected_val_in_select_reg_to_ctrl_val.items():

        if not isinstance(bin_val_in_select_reg, str):
            raise QuantestPyError(
                "val_in_select_reg as keys in "
                "expected_val_in_select_reg_to_ctrl_val must be string type."
            )
        if len(bin_val_in_select_reg) != len(select_reg):
            raise QuantestPyError(
                "Length of val_in_select_reg as keys in "
                "expected_val_in_select_reg_to_ctrl_val is not "
                "consistent with length of select_reg."
            )
        FastTestCircuit._assert_is_correct_qubit_val(
            qubit_val=[int(i) for i in bin_val_in_select_reg],
            qubit_val_name="val_in_select_reg"
        )
        if not isinstance(expected_ctrl_val, list) \
                and not isinstance(expected_ctrl_val, np.ndarray):
            raise QuantestPyError(
                "expected_ctrl_val as values in "
                "expected_val_in_select_reg_to_ctrl_val "
                "must be list or numpy.ndarray."
            )

        ctrl_val_of_all_ops = \
            _get_ctrl_val_of_all_ops_on_syst_reg_for_given_val_in_select_reg(
                bin_val_in_select_reg,
                ftc,
                select_reg,
                system_reg,
                ancilla_reg
            )

        if len(ctrl_val_of_all_ops) != len(expected_ctrl_val):
            err_msg = "The numbers of ops are not consistent " \
                + f"when val in select reg is {bin_val_in_select_reg}:\n" \
                + f"expect: {len(expected_ctrl_val)}\n" \
                + f"actual: {len(ctrl_val_of_all_ops)}"
            msg = ut_test_case._formatMessage(msg, err_msg)
            raise QuantestPyAssertionError(msg)

        if not np.allclose(ctrl_val_of_all_ops, expected_ctrl_val):
            err_msg = "Ctrl val(s) do not agree with your expectation " \
                + f"when val in select reg is {bin_val_in_select_reg}:\n" \
                + f"expect: {expected_ctrl_val}.\n" \
                + f"actual: {ctrl_val_of_all_ops}."
            msg = ut_test_case._formatMessage(msg, err_msg)
            raise QuantestPyAssertionError(msg)

        if assert_is_ancilla_uncomputated:
            if not np.all(ftc._qubit_value[ancilla_reg] == 0):
                err_msg = "ancilla reg is not uncomputated to 0 " \
                    + f"when val in select reg is {bin_val_in_select_reg}."
                msg = ut_test_case._formatMessage(msg, err_msg)
                raise QuantestPyAssertionError(msg)


def assert_get_ctrl_val(
        circuit: FastTestCircuit,
        select_reg: list,
        ancilla_reg: list = [],
        assert_is_ancilla_uncomputated: bool = False,
        verbose: bool = True) -> dict:

    # check inputs
    FastTestCircuit._assert_is_fast_test_circuit(circuit, "Input circuit")
    ftc = copy.deepcopy(circuit)
    ftc._assert_is_correct_reg(select_reg, "select_reg")
    ftc._assert_is_correct_reg(ancilla_reg, "ancilla_reg")

    len_select_reg = len(select_reg)
    qubit_idx_to_val_in_select_reg_to_ctrl_val = \
        {idx: dict() for idx in select_reg + ancilla_reg}

    for dec_val_in_select_reg in range(2**len_select_reg):

        bin_val_in_select_reg = \
            ("0" * len_select_reg + bin(dec_val_in_select_reg)[2:])[
                -len_select_reg:]

        qubit_idx_to_ctrl_val = \
            _get_qubit_idx_to_ctrl_val_for_given_val_in_select_reg(
                bin_val_in_select_reg,
                ftc,
                select_reg,
                ancilla_reg
            )

        if assert_is_ancilla_uncomputated:
            if not np.all(ftc._qubit_value[ancilla_reg] == 0):
                err_msg = "ancilla reg is not uncomputated to 0 " \
                    + f"when val in select reg is {bin_val_in_select_reg}."
                raise QuantestPyAssertionError(err_msg)

        if verbose:
            print(f"val in select reg: {bin_val_in_select_reg},",
                  f"qubit idx to ctrl val: {qubit_idx_to_ctrl_val}")

        for qubit_idx, ctrl_val in qubit_idx_to_ctrl_val.items():
            tmp_dict = qubit_idx_to_val_in_select_reg_to_ctrl_val[qubit_idx]
            tmp_dict[bin_val_in_select_reg] = ctrl_val
            qubit_idx_to_val_in_select_reg_to_ctrl_val[qubit_idx] = tmp_dict

    return qubit_idx_to_val_in_select_reg_to_ctrl_val
