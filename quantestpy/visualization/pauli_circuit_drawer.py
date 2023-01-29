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

        self._color_code_gate = self.get_color_code("blue")
        self._decimals = 2

        self._qubit_id_to_reg_name \
            = {qubit_id: "" for qubit_id in range(self._num_qubit)}
        self._qubit_id_to_output_reg_name \
            = {qubit_id: "" for qubit_id in range(self._num_qubit)}

    @staticmethod
    def add_color_code_in_obj(color_code: str, obj: str) -> str:
        return color_code + obj + "\033[0m"

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

    @staticmethod
    def get_tgt(name: str) -> str:
        """Overrides :
        Restricts gates to the gates implemented in PauliCircuit.
        """
        if name == "x":
            obj = "[X]"
        elif name == "y":
            obj = "[Y]"
        elif name == "z":
            obj = "[Z]"
        elif name == "swap":
            obj = "[SWP]"
        else:
            raise QuantestPyVisualizationError(
                f"Gate {name} is not implemented."
            )
        return obj

    @staticmethod
    def get_state(qubit_val: int) -> str:
        obj = "|1>" if qubit_val == 1 else "|0>"
        return obj

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

    def get_color_code_line(self, qubit_val: int) -> str:
        return self._color_code_line_1 if qubit_val == 1 else \
            self._color_code_line_0

    def get_phase(self, qubit_phase: float) -> str:
        phase_in_unit_of_pi = str(np.round(qubit_phase/np.pi, self._decimals))
        return phase_in_unit_of_pi

    def draw_qubit_init_identifier(self) -> None:
        """Overrides :
        Adds register names after qubit ids.
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
                self._line_id_to_text[line_id] += str(qubit_id) \
                    + self.get_space(id_max_length-len(str(qubit_id))) \
                    + reg_name \
                    + self.get_space(reg_name_max_length-len(reg_name))
            else:
                self._line_id_to_text[line_id] += \
                    self.get_space(id_max_length+reg_name_max_length)

    def draw_qubit_final_identifier(self) -> None:
        """Overrides :
        Adds register names before qubit ids.
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
                self._line_id_to_text[line_id] += reg_name \
                    + self.get_space(reg_name_max_length-len(reg_name)) \
                    + str(qubit_id) \
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
                obj = self.get_state(qubit_val)
            else:
                obj = self.get_space(length=3)
            self.add_obj_in_line_id_to_text(line_id, obj)

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
            phase_length = len(self.get_phase(qubit_phase))
            if phase_length > phase_max_length:
                phase_max_length = phase_length

        for line_id in range(self._num_line):
            if line_id in self._line_id_to_qubit_id.keys():
                qubit_id = self._line_id_to_qubit_id[line_id]
                qubit_phase = self._qc.qubit_phase[qubit_id]
                phase = self.get_phase(qubit_phase)
                obj = phase + self.get_space(phase_max_length-len(phase))
            else:
                obj = self.get_space(length=phase_max_length)
            self.add_obj_in_line_id_to_text(line_id, obj)

    def draw_final_phase(self) -> None:
        """Draws qubit phases in unit of PI.
        ::

        0.5
        """
        self.draw_init_phase()

    def color_line(self) -> None:
        """Colors lines according to their qubit values"""
        for line_id, text in self._line_id_to_text.items():
            if line_id in self._line_id_to_qubit_id.keys() and len(text) > 0:
                qubit_id = self._line_id_to_qubit_id[line_id]
                qubit_val = self._qc.qubit_value[qubit_id]
                color_code = self.get_color_code_line(qubit_val)
                obj = self.add_color_code_in_obj(color_code, text)
                self.add_obj_in_line_id_to_text(line_id, obj, replace_obj=True)

    def draw_one_gate(self, gate_id: int) -> None:
        """Overrides :
        Colors as well as draws objs for one gate operation.
        """
        # Set up
        self._gate_length = 0
        gate = self._qc.gates[gate_id]
        target_qubit_line_id = [self._qubit_id_to_line_id[qubit_id]
                                for qubit_id in gate["target_qubit"]]
        self._occupied_line_id = list()
        self.reset_line_id_to_text()

        # Target
        self.draw_tgt(gate_id)
        if self.is_gate_executed(gate_id):
            for line_id, text in self._line_id_to_text.items():
                if len(text) > 0:
                    obj = self.add_color_code_in_obj(
                        self._color_code_gate, text)
                    self.add_obj_in_line_id_to_text(
                        line_id, obj, replace_obj=True)
        self.update_line_id_to_text_whole()

        # Line or space
        line_id_list = list(range(self._num_line))
        for line_id in target_qubit_line_id:
            line_id_list.remove(line_id)  # remove lines of targets
        line_len = self._gate_length - 1
        line_len_fwd = int(line_len/2)
        line_len_bwd = line_len - line_len_fwd

        self.draw_line(line_id_list, line_len_fwd)
        self.color_line()
        self.update_line_id_to_text_whole()

        # Ctrl
        self.draw_ctrl(gate_id)
        for line_id, text in self._line_id_to_text.items():
            if len(text) > 0:
                if self.is_gate_executed(gate_id):
                    cc = self._color_code_gate
                else:
                    qubit_id = self._line_id_to_qubit_id[line_id]
                    qubit_val = self._qc.qubit_value[qubit_id]
                    cc = self.get_color_code_line(qubit_val)
                obj = self.add_color_code_in_obj(cc, text)
                self.add_obj_in_line_id_to_text(line_id, obj, replace_obj=True)
        self.update_line_id_to_text_whole()

        # Wire
        self.draw_wire(gate_id)
        if self.is_gate_executed(gate_id):
            for line_id, text in self._line_id_to_text.items():
                if len(text) > 0:
                    obj = self.add_color_code_in_obj(
                        self._color_code_gate, text)
                    self.add_obj_in_line_id_to_text(
                        line_id, obj, replace_obj=True)
        self.update_line_id_to_text_whole()

        # Line or space
        self.draw_rest()
        self.draw_line(line_id_list, line_len_bwd)
        self.color_line()
        self.update_line_id_to_text_whole()

        # Checker
        if len(self._occupied_line_id) != self._num_line:
            raise QuantestPyVisualizationError(
                "Unexpected error. Please report."
            )

    def draw_circuit(self) -> None:
        """Overrides :
        Calls the newly added draw methods.
        Colors the initial and final qubit lines.
        """
        self.draw_qubit_init_identifier()
        self.draw_space()
        self.draw_init_vector()
        self.draw_space()
        self.draw_init_phase()
        self.draw_space()
        self.update_line_id_to_text_whole()
        self.draw_line()
        self.color_line()
        self.update_line_id_to_text_whole()

        for i in range(len(self._qc.gates)):
            self.draw_one_gate(i)
            self._qc._execute_i_th_gate(i)

        self.draw_line()
        self.color_line()
        self.draw_space()
        self.draw_final_vector()
        self.draw_space()
        self.draw_final_phase()
        self.draw_space()
        self.draw_qubit_final_identifier()
        self.update_line_id_to_text_whole()


def draw_circuit(circuit: PauliCircuit) -> PauliCircuitDrawer:
    """This is the user interface."""
    PauliCircuit._assert_is_pauli_circuit(circuit)
    pcd = PauliCircuitDrawer(circuit)
    pcd.draw_circuit()
    return pcd
