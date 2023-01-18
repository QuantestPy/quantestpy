import numpy as np

from quantestpy.simulator.exceptions import PauliCircuitError
from quantestpy.simulator.quantestpy_circuit import QuantestPyCircuit

_IMPLEMENTED_GATES = ["x", "y", "z", "swap"]


class PauliCircuit(QuantestPyCircuit):

    def __init__(self, num_qubit: int):
        super().__init__(num_qubit=num_qubit)
        self._qubit_value = np.array([0 for _ in range(num_qubit)])
        self._qubit_phase = np.array([0. for _ in range(num_qubit)])

    @property
    def qubit_value(self,):
        return self._qubit_value

    @property
    def qubit_phase(self,):
        return self._qubit_phase

    @qubit_value.setter
    def qubit_value(self, value):
        self._qubit_value = value

    @qubit_phase.setter
    def qubit_phase(self, value):
        self._qubit_phase = value

    def _diagnostic_gate(self, gate: dict) -> None:
        """Override"""
        super()._diagnostic_gate(gate)

        if gate["name"] not in _IMPLEMENTED_GATES:
            raise PauliCircuitError(
                f'{gate["name"]} gate is not implemented.\n'
                f'Implemented gates: {_IMPLEMENTED_GATES}'
            )

        if "parameter" not in gate.keys():
            gate["parameter"] = []

    @staticmethod
    def _assert_is_pauli_circuit(circuit):
        if not isinstance(circuit, PauliCircuit):
            raise PauliCircuitError(
                "circuit must be an instance of PauliCircuit class."
            )

    def _assert_is_correct_reg(self, register):
        if not isinstance(register, list):
            raise PauliCircuitError("register must be a list.")

        for idx in register:
            if not isinstance(idx, int):
                raise PauliCircuitError(
                    "Indices in register must be integer type."
                )
            if idx >= self._num_qubit or idx < 0:
                raise PauliCircuitError(
                    f"Qubit index {idx} in register is out of range."
                )

    @staticmethod
    def _assert_is_correct_qubit_val(qubit_val):
        if not isinstance(qubit_val, list):
            raise PauliCircuitError("qubit_val must be a list.")

        for val in qubit_val:
            if not isinstance(val, int):
                raise PauliCircuitError(
                    "Values in qubit_val must be integer type."
                )
            if val not in [0, 1]:
                raise PauliCircuitError(
                    "Values in qubit_val must be either 0 or 1."
                )

    def _assert_is_correct_reg_and_qubit_val(self, register, qubit_val):
        self._assert_is_correct_reg(register)
        self._assert_is_correct_qubit_val(qubit_val)

        if len(register) != len(qubit_val):
            raise PauliCircuitError(
                "Length of register and that of qubit_val "
                "must be the same."
            )

    def set_qubit_value(self, qubit_idx: list, qubit_val: list):
        self._assert_is_correct_reg_and_qubit_val(
            register=qubit_idx,
            qubit_val=qubit_val
        )
        self._qubit_value[qubit_idx] = qubit_val

    def _execute_x_gate(self, target_qubit: list) -> None:
        self._qubit_value[target_qubit] ^= 1

    def _execute_y_gate(self, target_qubit: list) -> None:
        self._qubit_phase[target_qubit] \
            += np.pi * (0.5 - self._qubit_value[target_qubit])
        self._qubit_value[target_qubit] ^= 1

    def _execute_z_gate(self, target_qubit: list) -> None:
        self._qubit_phase[target_qubit] \
            += np.pi * self._qubit_value[target_qubit]

    def _execute_swap_gate(self, target_qubit: list) -> None:
        # swap qubit values
        a = self._qubit_value[target_qubit[0]]
        b = self._qubit_value[target_qubit[1]]
        self._qubit_value[target_qubit[0]] = b
        self._qubit_value[target_qubit[1]] = a
        # swap qubit phases
        a = self._qubit_phase[target_qubit[0]]
        b = self._qubit_phase[target_qubit[1]]
        self._qubit_phase[target_qubit[0]] = b
        self._qubit_phase[target_qubit[1]] = a

    def _execute_i_th_gate(self, i: int) -> None:
        gate = self._gates[i]
        if len(gate["control_qubit"]) == 0 or \
            np.all(self._qubit_value[gate["control_qubit"]]
                   == gate["control_value"]):

            if gate["name"] == "x":
                self._execute_x_gate(gate["target_qubit"])
            elif gate["name"] == "y":
                self._execute_y_gate(gate["target_qubit"])
            elif gate["name"] == "z":
                self._execute_z_gate(gate["target_qubit"])
            elif gate["name"] == "swap":
                self._execute_swap_gate(gate["target_qubit"])
            else:
                raise PauliCircuitError(
                    "Unexpected error. Please report."
                )

    def _execute_all_gates(self,) -> None:
        for i in range(len(self._gates)):
            self._execute_i_th_gate(i)

    def draw(self,):
        from quantestpy.visualization.pauli_circuit_drawer import draw_circuit

        return draw_circuit(self)


def cvt_quantestpy_circuit_to_pauli_circuit(
        qc: QuantestPyCircuit) -> PauliCircuit:
    """Converts an instance of QuantestPyCircuit to that of PauliCircuit.
    """
    if not isinstance(qc, QuantestPyCircuit):
        raise PauliCircuitError(
            "Input circuit must be an instance of QuantestPyCircuit."
        )

    pc = PauliCircuit(num_qubit=qc.num_qubit)
    for gate in qc.gates:
        pc.add_gate(gate)

    return pc
