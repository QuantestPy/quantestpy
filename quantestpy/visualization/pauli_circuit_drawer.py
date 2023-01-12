import numpy as np

from quantestpy.simulator.pauli_circuit import PauliCircuit
from quantestpy.visualization.exceptions import QuantestPyVisualizationError
from quantestpy.visualization.quantestpy_circuit_drawer import \
    QuantestPyCircuitDrawer


class PauliCircuitDrawer(QuantestPyCircuitDrawer):

    def __init__(self, circuit: PauliCircuit):
        PauliCircuit._assert_is_pauli_circuit(circuit)
        super().__init__(circuit)

        self._qubit_value = self._qc.qubit_value
        self._qubit_phase = self._qc.qubit_phase

        self._color_code_line_1 = self.get_color_code("green")
        self._color_code_line_0 = ""

        self._color_code_tgt = ""
        self._color_code_ctrl = ""
        self._color_code_cross = ""
        self._color_code_wire = ""
        self._color_code_gate = self.get_color_code("purple")
        self._decimals = 2

        self._qubit_id_to_color_code \
            = {qubit_id: "" for qubit_id in range(self._num_qubit)}
        self._output_qubit_id_to_color_code \
            = {qubit_id: "" for qubit_id in range(self._num_qubit)}

        self._qubit_id_to_reg_name \
            = {qubit_id: "" for qubit_id in range(self._num_qubit)}
        self._qubit_id_to_output_reg_name \
            = {qubit_id: "" for qubit_id in range(self._num_qubit)}

    @staticmethod
    def get_color_code(color: str) -> str:
        if color == "black":
            return "\033[30m"
        elif color == "red":
            return "\033[31m"
        elif color == "green":
            return "\033[32m"
        elif color == "yellow":
            return "\033[33m"
        elif color == "blue":
            return "\033[34m"
        elif color == "purple":
            return "\033[35m"
        elif color == "cyan":
            return "\033[36m"
        elif color == "white":
            return "\033[37m"
        elif color == "":
            return ""
        else:
            raise QuantestPyVisualizationError(f"{color} is invalid color.")

    def set_color_to_reg(self, color_to_reg: dict) -> None:
        for color, reg in color_to_reg.items():
            self._qc._assert_is_correct_reg(reg)
            for qubit_id in reg:
                self._qubit_id_to_color_code[qubit_id] = self.get_color_code(
                    color)

    def set_color_to_output_reg(self, color_to_reg: dict) -> None:
        for color, reg in color_to_reg.items():
            self._qc._assert_is_correct_reg(reg)
            for qubit_id in reg:
                self._output_qubit_id_to_color_code[qubit_id] = \
                    self.get_color_code(color)

    def set_name_to_reg(self, name_to_reg: dict) -> None:
        for name, reg in name_to_reg.items():
            self._qc._assert_is_correct_reg(reg)
            for qubit_id in reg:
                self._qubit_id_to_reg_name[qubit_id] = name

    def set_name_to_output_reg(self, name_to_reg: dict) -> None:
        for name, reg in name_to_reg.items():
            self._qc._assert_is_correct_reg(reg)
            for qubit_id in reg:
                self._qubit_id_to_output_reg_name[qubit_id] = name

    def is_gate_executed(self, gate_id: int) -> bool:
        gate = self._qc.gates[gate_id]
        if len(gate["control_qubit"]) == 0 or \
                np.all(self._qc.qubit_value[gate["control_qubit"]]
                       == gate["control_value"]):
            return True
        else:
            return False

    def reset_all(self,) -> None:
        super().reset_all()
        self._qc.qubit_value = self._qubit_value.copy()
        self._qc.qubit_phase = self._qubit_phase.copy()

    def get_color_code_line(self, qubit_val: int) -> str:
        return self._color_code_line_1 if qubit_val == 1 else \
            self._color_code_line_0

    @staticmethod
    def get_line(qubit_val: int, length: int = 3, color_code: str = "") -> str:
        _ = qubit_val  # unused
        return color_code + "─" * length + "\033[0m"

    @staticmethod
    def get_cross_line(qubit_val: int,
                       color_code_cross: str = "",
                       color_code_line: str = "") -> str:
        _ = qubit_val  # unused
        return color_code_line + "─" + "\033[0m" \
            + color_code_cross + "┼" + "\033[0m" \
            + color_code_line + "─" + "\033[0m"

    @staticmethod
    def get_wire(color_code: str = ""):
        return color_code + " │ " + "\033[0m"

    @staticmethod
    def get_tgt(name: str, qubit_val: int, color_code: str = "") -> str:
        _ = qubit_val  # unused
        if name == "x":
            obj = "[X]"
        elif name == "y":
            obj = "[Y]"
        elif name == "z":
            obj = "[Z]"
        elif name == "swap":
            obj = "SWP"
        else:
            raise QuantestPyVisualizationError(
                f"Gate {name} is not implemented."
            )
        return color_code + obj + "\033[0m"

    @staticmethod
    def get_ctrl(ctrl_val: int,
                 qubit_val: int,
                 color_code_ctrl: str = "",
                 color_code_line: str = "") -> str:
        _ = qubit_val  # unused
        obj = "■" if ctrl_val == 1 else "o"
        return color_code_line + "─" + "\033[0m" \
            + color_code_ctrl + obj + "\033[0m" \
            + color_code_line + "─" + "\033[0m"

    @staticmethod
    def get_state(qubit_val: int, color_code: str = "") -> str:
        obj = "|1>" if qubit_val == 1 else "|0>"
        return color_code + obj + "\033[0m"

    @staticmethod
    def get_phase(qubit_phase: float,
                  decimals: int,
                  color_code: str = "") -> str:
        qubit_phase_str = str(np.round(qubit_phase / np.pi, decimals))
        return color_code + qubit_phase_str + "\033[0m"

    def draw_qubit_init_identifier(self) -> None:
        """Overrides
        ::

        '0 reg1'

        '1     '
        """
        reg_name_max_length = 0
        for reg_name in self._qubit_id_to_reg_name.values():
            if len(reg_name) > reg_name_max_length:
                reg_name_max_length = len(reg_name)

        id_max_length = len(str(self._num_qubit-1))
        if reg_name_max_length > 0:
            id_max_length += 1

        for line_id in range(self._num_line):
            if line_id in self._line_id_to_qubit_id.keys():
                qubit_id = self._line_id_to_qubit_id[line_id]
                reg_name = self._qubit_id_to_reg_name[qubit_id]
                self._line_id_to_text[line_id] += \
                    self._qubit_id_to_color_code[qubit_id] \
                    + str(qubit_id) \
                    + self.get_space(id_max_length-len(str(qubit_id))) \
                    + reg_name \
                    + "\033[0m" \
                    + self.get_space(reg_name_max_length-len(reg_name))
            else:
                self._line_id_to_text[line_id] += \
                    self.get_space(id_max_length+reg_name_max_length)

    def draw_qubit_final_identifier(self) -> None:
        """Overrides
        ::
        'out 0'

        '    1'
        """
        reg_name_max_length = 0
        for reg_name in self._qubit_id_to_output_reg_name.values():
            if len(reg_name) > reg_name_max_length:
                reg_name_max_length = len(reg_name)

        if reg_name_max_length > 0:
            reg_name_max_length += 1

        id_max_length = len(str(self._num_qubit-1))
        for line_id in range(self._num_line):
            if line_id in self._line_id_to_qubit_id.keys():
                qubit_id = self._line_id_to_qubit_id[line_id]
                reg_name = self._qubit_id_to_output_reg_name[qubit_id]
                self._line_id_to_text[line_id] += \
                    self._output_qubit_id_to_color_code[qubit_id] \
                    + reg_name \
                    + self.get_space(reg_name_max_length-len(reg_name)) \
                    + str(qubit_id) \
                    + "\033[0m" \
                    + self.get_space(id_max_length-len(str(qubit_id)))
            else:
                self._line_id_to_text[line_id] += \
                    self.get_space(id_max_length+reg_name_max_length)

    def draw_init_vector(self) -> None:
        """Draws initial state vectors.
        ::

        |1>
        """
        for line_id in range(self._num_line):
            if line_id in self._line_id_to_qubit_id.keys():
                qubit_id = self._line_id_to_qubit_id[line_id]
                qubit_val = self._qc.qubit_value[qubit_id]
                self._line_id_to_text[line_id] += \
                    self.get_state(
                        qubit_val=qubit_val,
                        color_code=self.get_color_code_line(qubit_val))
            else:
                self._line_id_to_text[line_id] += self.get_space(length=3)

    def draw_final_vector(self) -> None:
        """Draws final state vectors.
        ::

        |0>
        """
        self.draw_init_vector()

    def draw_init_phase(self) -> None:
        """Draws qubit phases in unit of PI.
        ::

        0.0
        """
        phase_max_length = 0
        for qubit_phase in self._qc.qubit_phase:
            qubit_phase_str_length = \
                len(str(np.round(qubit_phase / np.pi, self._decimals)))
            if qubit_phase_str_length > phase_max_length:
                phase_max_length = qubit_phase_str_length

        for line_id in range(self._num_line):
            if line_id in self._line_id_to_qubit_id.keys():
                qubit_id = self._line_id_to_qubit_id[line_id]
                qubit_phase = self._qc.qubit_phase[qubit_id]
                qubit_phase_str = self.get_phase(qubit_phase, self._decimals)
                self._line_id_to_text[line_id] += qubit_phase_str \
                    + self.get_space(phase_max_length-len(qubit_phase_str))
            else:
                self._line_id_to_text[line_id] += self.get_space(
                    length=phase_max_length)

    def draw_final_phase(self) -> None:
        """Draws qubit phases in unit of PI.
        ::

        0.5
        """
        self.draw_init_phase()

    def draw_line(self) -> None:
        """Overrides"""
        for line_id in range(self._num_line):
            if line_id in self._line_id_to_qubit_id.keys():
                qubit_id = self._line_id_to_qubit_id[line_id]
                qubit_val = self._qc.qubit_value[qubit_id]
                cc = self.get_color_code_line(qubit_val)
                self._line_id_to_text[line_id] += \
                    self.get_line(qubit_val=qubit_val, length=1, color_code=cc)
            else:
                self._line_id_to_text[line_id] += self.get_space(length=1)

    def draw_tgt(self, gate_id: int) -> None:
        """Overrides"""
        if self.is_gate_executed(gate_id):
            self._color_code_tgt = self._color_code_gate
        else:
            self._color_code_tgt = ""

        gate = self._qc.gates[gate_id]
        for tg_qubit_id in gate["target_qubit"]:
            line_id = self._qubit_id_to_line_id[tg_qubit_id]
            qubit_val = self._qc.qubit_value[tg_qubit_id]
            self._line_id_to_text[line_id] += \
                self.get_tgt(
                    name=gate["name"],
                    qubit_val=qubit_val,
                    color_code=self._color_code_tgt)
            self._occupied_line_id.append(line_id)

    def draw_ctrl(self, gate_id: int) -> None:
        """Overrides"""
        if self.is_gate_executed(gate_id):
            self._color_code_ctrl = self._color_code_gate
        else:
            self._color_code_ctrl = ""

        gate = self._qc.gates[gate_id]
        for ctrl_qubit_id, ctrl_val \
                in zip(gate["control_qubit"], gate["control_value"]):
            line_id = self._qubit_id_to_line_id[ctrl_qubit_id]
            qubit_val = self._qc.qubit_value[ctrl_qubit_id]
            cc_ctrl = self._color_code_ctrl if \
                len(self._color_code_ctrl) > 0 \
                else self.get_color_code_line(qubit_val)
            cc_line = self.get_color_code_line(qubit_val)
            self._line_id_to_text[line_id] += self.get_ctrl(
                ctrl_val=ctrl_val,
                qubit_val=qubit_val,
                color_code_ctrl=cc_ctrl,
                color_code_line=cc_line
            )
            self._occupied_line_id.append(line_id)

    def draw_wire(self, gate_id: int) -> None:
        """Overrides"""
        if self.is_gate_executed(gate_id):
            self._color_code_wire = self._color_code_gate
            self._color_code_cross = self._color_code_gate
        else:
            self._color_code_wire = ""
            self._color_code_cross = ""

        gate = self._qc.gates[gate_id]
        inter_line_id = list()
        for ctrl_qubit_id in gate["control_qubit"]:
            ctrl_line_id = self._qubit_id_to_line_id[ctrl_qubit_id]
            for tg_qubit_id in gate["target_qubit"]:
                tg_line_id = self._qubit_id_to_line_id[tg_qubit_id]
                inter_line_id += self.get_inter_line_id(tg_line_id,
                                                        ctrl_line_id)

        for line_id in set(inter_line_id):
            # only when not occupied yet
            if line_id not in self._occupied_line_id:
                if line_id in self._line_id_to_qubit_id.keys():  # qubit
                    qubit_id = self._line_id_to_qubit_id[line_id]
                    qubit_val = self._qc.qubit_value[qubit_id]
                    cc_cross = self._color_code_cross
                    cc_line = self.get_color_code_line(qubit_val)
                    self._line_id_to_text[line_id] += self.get_cross_line(
                        qubit_val=qubit_val,
                        color_code_cross=cc_cross,
                        color_code_line=cc_line
                    )
                else:  # inter horizontal space
                    self._line_id_to_text[line_id] += \
                        self.get_wire(self._color_code_wire)
                self._occupied_line_id.append(line_id)

    def draw_rest(self, gate_id: int) -> None:
        """Overrides"""
        _ = gate_id  # unused
        for line_id in range(self._num_line):
            # only when not occupied yet
            if line_id not in self._occupied_line_id:
                if line_id in self._line_id_to_qubit_id.keys():  # qubit
                    qubit_id = self._line_id_to_qubit_id[line_id]
                    qubit_val = self._qc.qubit_value[qubit_id]
                    cc_line = self.get_color_code_line(qubit_val)
                    self._line_id_to_text[line_id] += \
                        self.get_line(qubit_val=qubit_val, color_code=cc_line)
                else:  # inter horizontal space
                    self._line_id_to_text[line_id] += self.get_space()
                self._occupied_line_id.append(line_id)

    def draw_circuit(self) -> None:
        """Overrides"""
        self.draw_qubit_init_identifier()
        self.draw_space()
        self.draw_init_vector()
        self.draw_space()
        self.draw_init_phase()
        self.draw_space()
        self.draw_line()

        for i in range(len(self._qc.gates)):
            self.draw_one_gate(i)
            self._qc._execute_i_th_gate(i)
            self.draw_line()

        self.draw_space()
        self.draw_final_vector()
        self.draw_space()
        self.draw_final_phase()
        self.draw_space()
        self.draw_qubit_final_identifier()


def draw_circuit(circuit: PauliCircuit) -> PauliCircuitDrawer:
    """This is the user interface."""
    PauliCircuit._assert_is_pauli_circuit(circuit)
    pcd = PauliCircuitDrawer(circuit)
    pcd.draw_circuit()
    return pcd
