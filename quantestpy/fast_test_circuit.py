import numpy as np

from quantestpy.exceptions import QuantestPyTestCircuitError
from quantestpy.test_circuit import TestCircuit

_IMPLEMENTED_GATES = ["x", "y", "z", "swap"]


class FastTestCircuit(TestCircuit):

    def __init__(self, num_qubit: int):
        super().__init__(num_qubit=num_qubit)
        self._qubit_value = np.array([0 for _ in range(num_qubit)])
        self._qubit_phase = np.array([0. for _ in range(num_qubit)])

    def add_gate(self, gate: dict) -> None:
        gate["parameter"] = []  # to avoid error
        if gate["name"] not in _IMPLEMENTED_GATES:
            raise QuantestPyTestCircuitError(
                f'{gate["name"]} is not implemented.'
                f'Implemented gates: {_IMPLEMENTED_GATES}'
            )
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
                "size of qubit_id must be the same with that of qubit_value."
            )

        for id in qubit_id:
            if not isinstance(id, int):
                raise QuantestPyTestCircuitError(
                    "elements in qubit_id must be integer."
                )

            if id >= self._num_qubit:
                raise QuantestPyTestCircuitError(
                    f"qubit_id {id} is out of range."
                )

        for value in qubit_value:
            if not isinstance(value, int):
                raise QuantestPyTestCircuitError(
                    "elements in qubit_value must be integer."
                )

            if value not in [0, 1]:
                raise QuantestPyTestCircuitError(
                    "elements in qubit_value must be either 0 or 1."
                )

        self._qubit_value[qubit_id] = qubit_value

    def set_qubit_phase(self, qubit_id: list, qubit_phase: list):
        if not isinstance(qubit_id, list):
            raise QuantestPyTestCircuitError(
                "qubit_id must be a list."
            )

        if not isinstance(qubit_phase, list):
            raise QuantestPyTestCircuitError(
                "qubit_phase must be a list."
            )

        if len(qubit_id) != len(qubit_phase):
            raise QuantestPyTestCircuitError(
                "size of qubit_id must be the same with that of qubit_phase."
            )

        for id in qubit_id:
            if not isinstance(id, int):
                raise QuantestPyTestCircuitError(
                    "elements in qubit_id must be integer."
                )

            if id >= self._num_qubit:
                raise QuantestPyTestCircuitError(
                    f"qubit_id {id} is out of range."
                )

        for phase in qubit_phase:
            if not isinstance(phase, int) and not isinstance(phase, float):
                raise QuantestPyTestCircuitError(
                    "elements in qubit_value must be real number."
                )

        self._qubit_phase[qubit_id] = qubit_phase

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
        a = self._qubit_value[target_qubit[0]]
        b = self._qubit_value[target_qubit[1]]
        self._qubit_value[target_qubit[0]] = b
        self._qubit_value[target_qubit[1]] = a

    def execute_all_gates(self,) -> None:
        for gate in self._gates:
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
                    raise


if __name__ == "__main__":
    """Example showing how to use FastTestCircuit class."""

    ftc = FastTestCircuit(5)
    ftc.add_gate({"name": "y", "target_qubit": [0], "control_qubit": [],
                  "control_value": [], "parameter": []})
    ftc.add_gate({"name": "x", "target_qubit": [1], "control_qubit": [],
                  "control_value": [], "parameter": []})
    ftc.add_gate({"name": "z", "target_qubit": [3], "control_qubit": [0, 1],
                  "control_value": [1, 1], "parameter": []})
    ftc.add_gate({"name": "swap", "target_qubit": [3, 1], "control_qubit": [0],
                  "control_value": [1], "parameter": []})

    ftc.execute_all_gates()
    print(ftc._qubit_value)
    print(ftc._qubit_phase)
