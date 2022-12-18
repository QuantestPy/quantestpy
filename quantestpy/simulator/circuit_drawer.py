import copy

from quantestpy.exceptions import QuantestPyError
from quantestpy.simulator.pauli_circuit import PauliCircuit


class CircuitDrawer:

    def __init__(self, pc: PauliCircuit):
        self._pc = copy.deepcopy(pc)
        self._qubit_value = pc._qubit_value.copy()
        self._qubit_phase = pc._qubit_phase.copy()

        self._color_code_line_1 = ""
        self._color_code_line_0 = ""

        self._color_code_tgt = ""
        self._color_code_ctrl = ""
        self._color_code_cross = ""
        self._color_code_wire = ""

        self._num_qubit = self._pc._num_qubit
        self._num_line = 2*self._num_qubit - 1
        self._qubit_id_to_line_id = {qubit_id: qubit_id * 2
                                     for qubit_id in range(self._num_qubit)}
        self._line_id_to_qubit_id \
            = {line_id: line_id // 2
               for line_id in range(self._num_line) if line_id % 2 == 0}
        self._line_id_to_text \
            = {line_id: "" for line_id in range(self._num_line)}
        self._qubit_id_to_color_code \
            = {qubit_id: "" for qubit_id in range(self._num_qubit)}
        self._qubit_id_to_reg_name \
            = {qubit_id: "" for qubit_id in range(self._num_qubit)}

        self._occupied_line_id = list()

    @property
    def line_id_to_text(self):
        return self._line_id_to_text

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
            raise QuantestPyError(f"{color} is invalid color.")

    def set_color_to_reg(self, color_to_reg: dict) -> None:
        for color, reg in color_to_reg.items():
            self._pc._assert_is_correct_reg(reg)
            for qubit_id in reg:
                self._qubit_id_to_color_code[qubit_id] = self.get_color_code(
                    color)

    def set_name_to_reg(self, name_to_reg: dict) -> None:
        for name, reg in name_to_reg.items():
            self._pc._assert_is_correct_reg(reg)
            for qubit_id in reg:
                self._qubit_id_to_reg_name[qubit_id] = name

    def reset_all(self,) -> None:
        self._line_id_to_text \
            = {line_id: "" for line_id in range(self._num_line)}
        self._pc._qubit_value = self._qubit_value.copy()
        self._pc._qubit_phase = self._qubit_phase.copy()

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
    def get_space(length: int = 3) -> str:
        return " " * length

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
            raise QuantestPyError(
                f"{name} is invalid input."
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
    def get_init_state(qubit_val: int, color_code: str = "") -> str:
        obj = "|1>" if qubit_val == 1 else "|0>"
        return color_code + obj + "\033[0m"

    @staticmethod
    def get_inter_line_id(id_a: int, id_b: int) -> list:
        id_max, id_min = max(id_a, id_b), min(id_a, id_b)
        return [id_ for id_ in range(id_max) if id_ < id_max and id_ > id_min]

    def draw_qubit_indentifier(self) -> None:
        """Draws a qubit identifer

        ::
        '0 reg1'

        '1     '
        """
        reg_name_max_length = 0
        for reg_name in self._qubit_id_to_reg_name.values():
            if len(reg_name) > reg_name_max_length:
                reg_name_max_length = len(reg_name)

        id_max_length = len(str(self._num_qubit-1))
        for line_id in range(self._num_line):
            if line_id in self._line_id_to_qubit_id.keys():
                qubit_id = self._line_id_to_qubit_id[line_id]
                reg_name = self._qubit_id_to_reg_name[qubit_id]
                self._line_id_to_text[line_id] += \
                    self._qubit_id_to_color_code[qubit_id] \
                    + str(qubit_id) \
                    + self.get_space(id_max_length+1-len(str(qubit_id))) \
                    + reg_name \
                    + "\033[0m" \
                    + self.get_space(reg_name_max_length-len(reg_name))
            else:
                self._line_id_to_text[line_id] += \
                    self.get_space(id_max_length+1+reg_name_max_length)

    def draw_init_vector(self) -> None:
        """Draws initial state vectors.

        ::
        |1>

        |0>
        """
        for line_id in range(self._num_line):
            if line_id in self._line_id_to_qubit_id.keys():
                qubit_id = self._line_id_to_qubit_id[line_id]
                qubit_val = self._pc._qubit_value[qubit_id]
                self._line_id_to_text[line_id] += \
                    self.get_init_state(
                        qubit_val=qubit_val,
                        color_code=self.get_color_code_line(qubit_val))
            else:
                self._line_id_to_text[line_id] += self.get_space(length=3)

    def draw_space(self,) -> None:
        """Draws spaces.

        ::
        ' '
        """
        for line_id in range(self._num_line):
            self._line_id_to_text[line_id] += self.get_space(length=1)

    def draw_line(self) -> None:
        """Draws lines.

        ::
        ─

        ─

        ─
        """
        for line_id in range(self._num_line):
            if line_id in self._line_id_to_qubit_id.keys():
                qubit_id = self._line_id_to_qubit_id[line_id]
                qubit_val = self._pc._qubit_value[qubit_id]
                cc = self.get_color_code_line(qubit_val)
                self._line_id_to_text[line_id] += \
                    self.get_line(qubit_val=qubit_val, length=1, color_code=cc)
            else:
                self._line_id_to_text[line_id] += self.get_space(length=1)

    def draw_tgt(self, gate_id: int) -> None:
        """Draws target objs in a gate.

        ::
        [X]

        [X]
        """
        gate = self._pc._gates[gate_id]
        for tg_qubit_id in gate["target_qubit"]:
            line_id = self._qubit_id_to_line_id[tg_qubit_id]
            qubit_val = self._pc._qubit_value[tg_qubit_id]
            self._line_id_to_text[line_id] += \
                self.get_tgt(
                    name=gate["name"],
                    qubit_val=qubit_val,
                    color_code=self._color_code_tgt)
            self._occupied_line_id.append(line_id)

    def draw_ctrl(self, gate_id: int) -> None:
        """Draws ctrl objs in a gate.

        ::
        ─■─

        ─■─
        """
        gate = self._pc._gates[gate_id]
        for ctrl_qubit_id, ctrl_val \
                in zip(gate["control_qubit"], gate["control_value"]):
            line_id = self._qubit_id_to_line_id[ctrl_qubit_id]
            qubit_val = self._pc._qubit_value[ctrl_qubit_id]
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
        """Draws wire objs between tgt and ctrl objs in a gate.

        ::
         │
         ┼
         │
        """
        gate = self._pc._gates[gate_id]
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
                    qubit_val = self._pc._qubit_value[qubit_id]
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
        """Draws objs to fill the holes.

        ::
        '   '

        """
        _ = gate_id  # unused
        for line_id in range(self._num_line):
            # only when not occupied yet
            if line_id not in self._occupied_line_id:
                if line_id in self._line_id_to_qubit_id.keys():  # qubit
                    qubit_id = self._line_id_to_qubit_id[line_id]
                    qubit_val = self._pc._qubit_value[qubit_id]
                    cc_line = self.get_color_code_line(qubit_val)
                    self._line_id_to_text[line_id] += \
                        self.get_line(qubit_val=qubit_val, color_code=cc_line)
                else:  # inter horizontal space
                    self._line_id_to_text[line_id] += self.get_space()
                self._occupied_line_id.append(line_id)

    def draw_one_gate(self, gate_id: int) -> None:
        """Draws objs for one gate operation.

        ::
        ─■─
         │
        ─┼─
         │
        ─o─
         │
        [X]

        ───
        """
        self._occupied_line_id = list()
        self.draw_tgt(gate_id)
        self.draw_ctrl(gate_id)
        self.draw_wire(gate_id)
        self.draw_rest(gate_id)

        if len(self._occupied_line_id) != self._num_line:
            raise QuantestPyError("Unexpected error. Please report.")

    def draw_circuit(self) -> None:
        """Draw all objs for the circuit

        ::
        0  |1> ──■──────[X]─
                 │       │
        1  |0> ──┼───────┼──
                 │       │
        2  |1> ──o───■───■──
                 │   │   │
        3  |1> ─[X]──o───┼──
                     │   │
        4  |1> ─────[X]──■──
        """
        self.draw_qubit_indentifier()
        self.draw_space()
        self.draw_init_vector()
        self.draw_space()
        self.draw_line()

        for i in range(len(self._pc._gates)):
            self.draw_one_gate(i)
            self._pc._execute_i_th_gate(i)
            self.draw_line()

    def create_single_string(self) -> str:
        return "\n".join(list(self.line_id_to_text.values()))

    def __repr__(self) -> str:
        return self.create_single_string()

    def __str__(self) -> str:
        return self.create_single_string()


def draw_circuit(circuit: PauliCircuit) -> CircuitDrawer:
    """This is the user interface."""
    PauliCircuit._assert_is_pauli_circuit(circuit)
    cd = CircuitDrawer(circuit)
    cd.draw_circuit()
    return cd
