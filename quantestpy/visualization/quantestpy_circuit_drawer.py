import copy

from quantestpy.simulator.quantestpy_circuit import QuantestPyCircuit
from quantestpy.visualization.exceptions import QuantestPyVisualizationError


class QuantestPyCircuitDrawer:

    def __init__(self, circuit: QuantestPyCircuit):
        self._qc = copy.deepcopy(circuit)

        self._num_qubit = self._qc.num_qubit
        self._num_line = 2*self._num_qubit - 1
        self._qubit_id_to_line_id = {qubit_id: qubit_id * 2
                                     for qubit_id in range(self._num_qubit)}
        self._line_id_to_qubit_id \
            = {line_id: line_id // 2
               for line_id in range(self._num_line) if line_id % 2 == 0}
        self._line_id_to_text \
            = {line_id: "" for line_id in range(self._num_line)}
        self._occupied_line_id = list()

    @property
    def line_id_to_text(self):
        return self._line_id_to_text

    def reset_all(self,) -> None:
        self._line_id_to_text \
            = {line_id: "" for line_id in range(self._num_line)}

    @staticmethod
    def get_line(length: int = 3) -> str:
        return "─" * length

    @staticmethod
    def get_cross_line() -> str:
        return "─┼─"

    @staticmethod
    def get_wire():
        return " │ "

    @staticmethod
    def get_space(length: int = 3) -> str:
        return " " * length

    @staticmethod
    def get_tgt(name: str) -> str:
        if name == "id":
            obj = "[I]"
        elif name == "x":
            obj = "[X]"
        elif name == "y":
            obj = "[Y]"
        elif name == "z":
            obj = "[Z]"
        elif name == "h":
            obj = "[H]"
        elif name == "s":
            obj = "[S]"
        elif name == "sdg":
            obj = "S^+"
        elif name == "t":
            obj = "[T]"
        elif name == "tdg":
            obj = "T^+"
        elif name == "swap":
            obj = "SWP"
        elif name == "iswap":
            obj = "iSW"
        elif name == "rx":
            obj = "R_x"
        elif name == "ry":
            obj = "R_y"
        elif name == "rz":
            obj = "R_z"
        elif name == "r":
            obj = "[R]"
        elif name == "p":
            obj = "[P]"
        elif name == "scalar":
            obj = "SCL"
        elif name == "u":
            obj = "[U]"
        else:
            raise QuantestPyVisualizationError(
                f"Gate {name} is not inplemented."
            )
        return obj

    @staticmethod
    def get_ctrl(ctrl_val: int) -> str:
        obj = "■" if ctrl_val == 1 else "o"
        return "─" + obj + "─"

    @staticmethod
    def get_inter_line_id(id_a: int, id_b: int) -> list:
        id_max, id_min = max(id_a, id_b), min(id_a, id_b)
        return [id_ for id_ in range(id_max) if id_ < id_max and id_ > id_min]

    def draw_qubit_init_identifier(self) -> None:
        """Draws a qubit identifer
        ::

        '0'

        '1'
        """
        id_max_length = len(str(self._num_qubit-1))
        for line_id in range(self._num_line):
            if line_id in self._line_id_to_qubit_id.keys():
                qubit_id = self._line_id_to_qubit_id[line_id]
                self._line_id_to_text[line_id] += str(qubit_id) \
                    + self.get_space(id_max_length-len(str(qubit_id)))
            else:
                self._line_id_to_text[line_id] += self.get_space(id_max_length)

    def draw_qubit_final_identifier(self) -> None:
        """Draws a qubit identifer at the end
        ::

        '0'

        '1'
        """
        self.draw_qubit_init_identifier()

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
        """
        for line_id in range(self._num_line):
            if line_id in self._line_id_to_qubit_id.keys():
                self._line_id_to_text[line_id] += self.get_line(length=1)
            else:
                self._line_id_to_text[line_id] += self.get_space(length=1)

    def draw_tgt(self, gate_id: int) -> None:
        """Draws target objs in a gate.
        ::

        [X]
        """
        gate = self._qc.gates[gate_id]
        for tg_qubit_id in gate["target_qubit"]:
            line_id = self._qubit_id_to_line_id[tg_qubit_id]
            self._line_id_to_text[line_id] += self.get_tgt(name=gate["name"])
            self._occupied_line_id.append(line_id)

    def draw_ctrl(self, gate_id: int) -> None:
        """Draws ctrl objs in a gate.
        ::

        ─■─
        """
        gate = self._qc.gates[gate_id]
        for ctrl_qubit_id, ctrl_val \
                in zip(gate["control_qubit"], gate["control_value"]):
            line_id = self._qubit_id_to_line_id[ctrl_qubit_id]
            self._line_id_to_text[line_id] += self.get_ctrl(ctrl_val=ctrl_val)
            self._occupied_line_id.append(line_id)

    def draw_wire(self, gate_id: int) -> None:
        """Draws wire objs between tgt and ctrl objs in a gate.
        ::

         │
         ┼
         │
        """
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
                    self._line_id_to_text[line_id] += self.get_cross_line()
                else:  # inter horizontal space
                    self._line_id_to_text[line_id] += self.get_wire()
                self._occupied_line_id.append(line_id)

    def draw_rest(self, gate_id: int) -> None:
        """Draws lines or puts spaces to fill the holes.
        ::

        '   '

        '───'
        """
        _ = gate_id  # unused
        for line_id in range(self._num_line):
            # only when not occupied yet
            if line_id not in self._occupied_line_id:
                if line_id in self._line_id_to_qubit_id.keys():  # qubit
                    self._line_id_to_text[line_id] += self.get_line()
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
            raise QuantestPyVisualizationError(
                "Unexpected error. Please report."
            )

    def draw_circuit(self) -> None:
        """Draw all objs for the circuit
        ::

        0 ──■──────[X]─
            │       │
        1 ──┼───────┼──
            │       │
        2 ──o───■───■──
            │   │   │
        3 ─[X]──o───┼──
                │   │
        4 ─────[X]──■──
        """
        self.draw_qubit_init_identifier()
        self.draw_space()
        self.draw_line()

        for i in range(len(self._qc.gates)):
            self.draw_one_gate(i)
            self.draw_line()

        self.draw_space()
        self.draw_qubit_final_identifier()

    def create_single_string(self) -> str:
        return "\n".join(list(self.line_id_to_text.values()))

    def __repr__(self) -> str:
        return self.create_single_string()

    def __str__(self) -> str:
        return self.create_single_string()


def draw_circuit(circuit: QuantestPyCircuit) -> QuantestPyCircuitDrawer:
    """This is the user interface."""
    qcd = QuantestPyCircuitDrawer(circuit)
    qcd.draw_circuit()
    return qcd
