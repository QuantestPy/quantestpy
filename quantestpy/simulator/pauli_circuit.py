import numpy as np

from quantestpy.exceptions import QuantestPyError, QuantestPyTestCircuitError
from quantestpy.test_circuit import TestCircuit

_IMPLEMENTED_GATES = ["x", "y", "z", "swap"]


class PauliCircuit(TestCircuit):

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

    @staticmethod
    def _assert_is_pauli_circuit(circuit, circuit_name: str):
        if not isinstance(circuit, PauliCircuit):
            raise QuantestPyTestCircuitError(
                f"{circuit_name} must be an instance of PauliCircuit class."
            )

    def _assert_is_correct_reg(self, reg, reg_name: str):
        if not isinstance(reg, list):
            raise QuantestPyTestCircuitError(f"{reg_name} must be a list.")

        for idx in reg:
            if not isinstance(idx, int):
                raise QuantestPyTestCircuitError(
                    f"Indices in {reg_name} must be integer type."
                )
            if idx >= self._num_qubit or idx < 0:
                raise QuantestPyTestCircuitError(
                    f"Qubit index {idx} in {reg_name} is out of range."
                )

    @staticmethod
    def _assert_is_correct_qubit_val(qubit_val, qubit_val_name: str):
        if not isinstance(qubit_val, list):
            raise QuantestPyTestCircuitError(
                f"{qubit_val_name} must be a list."
            )

        for val in qubit_val:
            if not isinstance(val, int):
                raise QuantestPyTestCircuitError(
                    f"Values in {qubit_val_name} must be integer type."
                )
            if val not in [0, 1]:
                raise QuantestPyTestCircuitError(
                    f"Values in {qubit_val_name} must be either 0 or 1."
                )

    def _assert_is_correct_reg_and_qubit_val(
            self, reg, reg_name, qubit_val, qubit_val_name):
        self._assert_is_correct_reg(reg, reg_name)
        self._assert_is_correct_qubit_val(qubit_val, qubit_val_name)

        if len(reg) != len(qubit_val):
            raise QuantestPyTestCircuitError(
                f"Length of {reg_name} and that of {qubit_val_name} "
                "must be the same."
            )

    def set_qubit_value(self, qubit_idx: list, qubit_val: list):
        self._assert_is_correct_reg_and_qubit_val(
            reg=qubit_idx,
            reg_name="qubit_idx",
            qubit_val=qubit_val,
            qubit_val_name="qubit_val"
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
                raise QuantestPyError("Unexpected error. Please report.")

    def _execute_all_gates(self,) -> None:
        for i in range(len(self._gates)):
            self._execute_i_th_gate(i)
