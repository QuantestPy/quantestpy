import copy
import sys

import numpy as np

from quantestpy import PauliCircuit
from quantestpy.exceptions import QuantestPyError
from quantestpy.simulator.circuit_drawer import CircuitDrawer


class CircuitDrawerGateColoring(CircuitDrawer):
    def __init__(self, pc: PauliCircuit):
        super().__init__(pc)
        self._color_code_line_1 = self.get_color_code("green")
        self._color_code_gate = self.get_color_code("red")

    def is_gate_executed(self, gate_id: int) -> bool:
        gate = self._pc._gates[gate_id]
        if len(gate["control_qubit"]) == 0 or \
                np.all(self._pc._qubit_value[gate["control_qubit"]]
                       == gate["control_value"]):
            return True
        else:
            return False

    def draw_tgt(self, gate_id: int) -> None:
        """Draws target objs in a gate.

        ::
        [X]

        [X]
        """
        if self.is_gate_executed(gate_id):
            self._color_code_tgt = self._color_code_gate
        else:
            self._color_code_tgt = ""
        super().draw_tgt(gate_id)

    def draw_ctrl(self, gate_id: int) -> None:
        """Draws ctrl objs in a gate.

        ::
        ─■─

        ─■─
        """
        if self.is_gate_executed(gate_id):
            self._color_code_ctrl = self._color_code_gate
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
        if self.is_gate_executed(gate_id):
            self._color_code_wire = self._color_code_gate
            self._color_code_cross = self._color_code_gate
        else:
            self._color_code_wire = ""
            self._color_code_cross = ""
        super().draw_wire(gate_id)


def assert_color_ctrl_val(
        circuit: PauliCircuit,
        ctrl_reg: list,
        ancilla_reg: list = [],
        val_in_ctrl_reg_list: list = []):

    # check inputs
    PauliCircuit._assert_is_pauli_circuit(circuit)
    circuit._assert_is_correct_reg(ctrl_reg)
    circuit._assert_is_correct_reg(ancilla_reg)
    if not isinstance(val_in_ctrl_reg_list, list):
        raise QuantestPyError("val_in_ctrl_reg_list must be a list.")

    len_ctrl_reg = len(ctrl_reg)
    for val in val_in_ctrl_reg_list:
        if not isinstance(val, str):
            raise QuantestPyError(
                "Elements in val_in_ctrl_reg_list must be strings."
            )
        if len(val) != len_ctrl_reg:
            raise QuantestPyError(
                f"Element {val} in val_in_ctrl_reg_list has an invalid length."
            )

    def _draw_circuit(val_in_ctrl_reg: str):
        # define the circuit
        pc = copy.deepcopy(circuit)
        pc.set_qubit_value(ancilla_reg, [0] * len(ancilla_reg))
        pc.set_qubit_value(ctrl_reg, [int(i) for i in val_in_ctrl_reg])

        # create an instance of CircuitDrawer
        gc = CircuitDrawerGateColoring(pc=pc)
        gc.set_name_to_reg({"ctrl": ctrl_reg, "anci": ancilla_reg})
        gc.set_color_to_reg({"blue": ctrl_reg, "purple": ancilla_reg})
        gc.draw_circuit()
        length = len(list(gc.line_id_to_text.values()))
        fig = gc.create_single_string()

        # show result
        print(val_in_ctrl_reg)
        print(fig)
        input("enter")
        sys.stdout.write(f"\033[{length+2}F")
        sys.stdout.write("\033[2K")
        del pc, gc
        return

    if len(val_in_ctrl_reg_list) == 0:
        for dec_val_in_ctrl_reg in range(2**len_ctrl_reg):
            val_in_ctrl_reg = ("0" * len_ctrl_reg +
                               bin(dec_val_in_ctrl_reg)[2:])[-len_ctrl_reg:]
            _draw_circuit(val_in_ctrl_reg)

    else:
        for val_in_ctrl_reg in val_in_ctrl_reg_list:
            _draw_circuit(val_in_ctrl_reg)
