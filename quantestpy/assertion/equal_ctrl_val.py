import copy
import sys
from typing import Union

import numpy as np

from quantestpy import PauliCircuit
from quantestpy.exceptions import QuantestPyAssertionError, QuantestPyError
from quantestpy.simulator.circuit_drawer import CircuitDrawer


def _is_a_in_b(a: list, b: list) -> bool:
    for i in a:
        if i in b:
            return True
    return False


class CircuitDrawerErrorGateColoring(CircuitDrawer):
    def __init__(self, pc: PauliCircuit, err_gate_id_lst: list):
        super().__init__(pc)
        self._color_code_line_1 = self.get_color_code("green")

        self._color_code_error = self.get_color_code("red")
        self._err_gate_id_lst = err_gate_id_lst

    def is_gate_error(self, gate_id: int) -> bool:
        return True if gate_id in self._err_gate_id_lst else False

    def draw_tgt(self, gate_id: int) -> None:
        """Draws target objs in a gate.
        ::
        [X]

        [X]
        """
        if self.is_gate_error(gate_id):
            self._color_code_tgt = self._color_code_error
        else:
            self._color_code_tgt = ""
        super().draw_tgt(gate_id)

    def draw_ctrl(self, gate_id: int) -> None:
        """Draws ctrl objs in a gate.
        ::
        ─■─

        ─■─
        """
        if self.is_gate_error(gate_id):
            self._color_code_ctrl = self._color_code_error
        else:
            self._color_code_ctrl = ""
        super().draw_ctrl(gate_id)

    def draw_wire(self, gate_id: int) -> None:
        """Draws wire objs between tgt and ctrl objs in a gate.
        ::
         │
         ┼
         │
        """
        if self.is_gate_error(gate_id):
            self._color_code_wire = self._color_code_error
            self._color_code_cross = self._color_code_error
        else:
            self._color_code_wire = ""
            self._color_code_cross = ""
        super().draw_wire(gate_id)


def assert_equal_ctrl_val(
        circuit: PauliCircuit,
        ctrl_reg: list,
        val_in_ctrl_reg_to_is_gate_executed_expect: dict,
        ancilla_reg: list = [],
        tgt_reg: list = [],
        draw_circuit: bool = False,
        check_ancilla_is_uncomputed: bool = False):

    # check inputs
    PauliCircuit._assert_is_pauli_circuit(circuit)
    pc = copy.deepcopy(circuit)
    pc._assert_is_correct_reg(ctrl_reg)
    pc._assert_is_correct_reg(ancilla_reg)
    pc._assert_is_correct_reg(tgt_reg)

    if not isinstance(val_in_ctrl_reg_to_is_gate_executed_expect, dict):
        raise QuantestPyError(
            "val_in_ctrl_reg_to_is_gate_executed_expect must be a dict."
        )
    if not isinstance(draw_circuit, bool):
        raise QuantestPyError("draw_circuit must be bool type.")

    if len(tgt_reg) == 0:
        tgt_reg = [id for id in range(pc._num_qubit)
                   if id not in ctrl_reg + ancilla_reg]

    def _assert_equal(val_in_ctrl_reg: str, is_gate_executed_expect: list) \
            -> Union[None, tuple]:
        # define the circuit object
        pc = copy.deepcopy(circuit)
        pc.set_qubit_value(ancilla_reg, [0] * len(ancilla_reg))
        pc.set_qubit_value(ctrl_reg, [int(i) for i in val_in_ctrl_reg])

        def is_gate_executed(gate: dict) -> int:
            if len(gate["control_qubit"]) == 0 or \
                    np.all(pc._qubit_value[gate["control_qubit"]]
                           == gate["control_value"]):
                return 1
            else:
                return 0

        is_gate_executed_actual, gate_id_lst = list(), list()
        for i, gate in enumerate(pc._gates):
            tgt_qubit_idx = gate["target_qubit"]
            if _is_a_in_b(a=tgt_qubit_idx, b=tgt_reg):
                is_gate_executed_actual.append(is_gate_executed(gate))
                gate_id_lst.append(i)

            pc._execute_i_th_gate(i)

        if len(is_gate_executed_expect) != len(is_gate_executed_actual):
            raise QuantestPyError(
                "length of is_gate_executed_expect is illegal."
            )

        if check_ancilla_is_uncomputed:
            if not np.all(pc._qubit_value[ancilla_reg] == 0):
                err_msg = "ancilla reg is not back to 0 by uncomputation " \
                    + f"when val in ctrl reg is {val_in_ctrl_reg}."
                raise QuantestPyAssertionError(err_msg)

        del pc

        if is_gate_executed_actual == is_gate_executed_expect:
            return None

        else:
            err_gate_id_lst = list()
            for i, (act, exp) in enumerate(
                    zip(is_gate_executed_actual, is_gate_executed_expect)):
                if act != exp:
                    err_gate_id_lst.append(gate_id_lst[i])

            return (is_gate_executed_actual, err_gate_id_lst)

    def _draw_circuit(val_in_ctrl_reg: str, err_gate_id_lst: list):
        # define the circuit object
        pc = copy.deepcopy(circuit)
        pc.set_qubit_value(ancilla_reg, [0] * len(ancilla_reg))
        pc.set_qubit_value(ctrl_reg, [int(i) for i in val_in_ctrl_reg])

        # create an instance of CircuitDrawerCtrlColoring
        cd = CircuitDrawerErrorGateColoring(
            pc=pc,
            err_gate_id_lst=err_gate_id_lst
        )
        cd.set_name_to_reg({"ctrl": ctrl_reg, "anci": ancilla_reg})
        cd.set_color_to_reg({"blue": ctrl_reg, "purple": ancilla_reg})
        cd.draw_circuit()
        length = len(list(cd.line_id_to_text.values()))
        fig = cd.create_single_string()

        # show result
        print(val_in_ctrl_reg)
        print(fig)
        input("press enter")
        sys.stdout.write(f"\033[{length+2}F")
        sys.stdout.write("\033[2K")
        del pc, cd
        return

    len_ctrl_reg = len(ctrl_reg)
    for val, is_gate_executed_expect in \
            val_in_ctrl_reg_to_is_gate_executed_expect.items():

        # check inputs
        if not isinstance(val, str):
            raise QuantestPyError(
                "Key in val_in_ctrl_reg_to_is_gate_executed_expect must "
                "be a string."
            )
        if len(val) != len_ctrl_reg:
            raise QuantestPyError(
                f"Key {val} in val_in_ctrl_reg_to_is_gate_executed_expect "
                "has an invalid length."
            )
        if not isinstance(is_gate_executed_expect, list):
            raise QuantestPyError(
                "Value in val_in_ctrl_reg_to_is_gate_executed_expect must "
                "be a list."
            )
        for i in is_gate_executed_expect:
            if not isinstance(i, int) or i not in [0, 1]:
                raise QuantestPyError(
                    "Element in is_gate_executed_expect must be an integer of "
                    "either 1 or 0, where 1 indicates that the gate is "
                    "executed while 0 not executed."
                )

        # Invoke the assert equal
        output_from_assert_equal = _assert_equal(val, is_gate_executed_expect)

        if output_from_assert_equal is not None:
            is_gate_executed_actual, err_gate_id_lst = output_from_assert_equal
            if draw_circuit:
                _draw_circuit(val, err_gate_id_lst)
            else:
                raise QuantestPyAssertionError(
                    f"val_in_ctrl_reg: {val}\n"
                    f"is_gate_executed_expect: {is_gate_executed_expect}\n"
                    f"is_gate_executed_actual: {is_gate_executed_actual}"
                )
