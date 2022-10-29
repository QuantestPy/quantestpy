import numpy as np

from quantestpy.exceptions import QuantestPyError, QuantestPyTestCircuitError
from quantestpy.test_circuit import TestCircuit

_IMPLEMENTED_GATES = ["x", "y", "z", "swap"]


class FastTestCircuit(TestCircuit):

    def __init__(self, num_qubit: int):
        if not isinstance(num_qubit, int) or num_qubit < 1:
            raise QuantestPyTestCircuitError(
                "num_qubit must be an integer greater than 0."
            )

        super().__init__(num_qubit=num_qubit)
        self._qubit_value = np.array([0 for _ in range(num_qubit)])
        self._qubit_phase = np.array([0. for _ in range(num_qubit)])

    def add_gate(self, gate: dict) -> None:
        if not isinstance(gate, dict):
            raise QuantestPyTestCircuitError(
                "gate must be a dictionary which contains 'name', "
                "'target_qubit', 'control_qubit' and 'control_value' as keys."
            )

        if "name" not in gate.keys():
            raise QuantestPyTestCircuitError(
                "gate must contain 'name' as a key."
            )

        if gate["name"] not in _IMPLEMENTED_GATES:
            raise QuantestPyTestCircuitError(
                f'{gate["name"]} gate is not implemented.\n'
                f'Implemented gates: {_IMPLEMENTED_GATES}'
            )

        gate["parameter"] = []  # to avoid raise in TestCircuit.add_gate()
        super().add_gate(gate=gate)

    def set_qubit_value(self, qubit_id: list, qubit_value: list):
        if not isinstance(qubit_id, list):
            raise QuantestPyTestCircuitError(
                "qubit_id must be a list."
            )

        if not isinstance(qubit_value, list):
            raise QuantestPyTestCircuitError(
                "qubit_value must be a list."
            )

        if len(qubit_id) != len(qubit_value):
            raise QuantestPyTestCircuitError(
                "Lenght of qubit_id and that of qubit_value must be same."
            )

        for id in qubit_id:
            if not isinstance(id, int):
                raise QuantestPyTestCircuitError(
                    "Elements in qubit_id must be integer type."
                )
            if id >= self._num_qubit or id < 0:
                raise QuantestPyTestCircuitError(
                    f"qubit_id {id} is out of range."
                )

        for value in qubit_value:
            if not isinstance(value, int):
                raise QuantestPyTestCircuitError(
                    "Elements in qubit_value must be integer type."
                )
            if value not in [0, 1]:
                raise QuantestPyTestCircuitError(
                    "Elements in qubit_value must be either 0 or 1."
                )

        self._qubit_value[qubit_id] = qubit_value

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
                raise QuantestPyError("Unexpected error. Please report.")

    def _execute_all_gates(self,) -> None:
        for i in range(len(self._gates)):
            self._execute_i_th_gate(i)
