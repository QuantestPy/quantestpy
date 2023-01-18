from quantestpy.simulator.exceptions import QuantestPyCircuitError


class QuantestPyCircuit:
    """
    This class will be used as a base circuit class for other
    circuit classes.
    """

    def __init__(self, num_qubit: int):
        if not isinstance(num_qubit, int) or num_qubit < 1:
            raise QuantestPyCircuitError(
                "num_qubit must be an integer greater than 0."
            )
        self._gates = []
        self._qubit_indices = [i for i in range(num_qubit)]
        self._num_qubit = num_qubit

    @property
    def gates(self):
        return self._gates

    @property
    def num_qubit(self):
        return self._num_qubit

    @property
    def qubit_indices(self):
        return self._qubit_indices

    def _diagnostic_gate(self, gate: dict) -> None:
        """
        Example
        gate = {"name": "x", "target_qubit": [1], "control_qubit": [],
                "control_value": [], "parameter": []}
        gate = {"name": "rx", "target_qubit": [1], "control_qubit": [0],
                "control_value": [1], "parameter": [np.pi/8]}
        """
        if not isinstance(gate, dict):
            raise QuantestPyCircuitError(
                "gate's type must be dictionary which contains 'name', "
                "'target_qubit' and optionally 'control_qubit' as keys."
            )

        if "name" not in gate.keys():
            raise QuantestPyCircuitError(
                "gate must contain 'name' as a key."
            )

        if "target_qubit" not in gate.keys():
            raise QuantestPyCircuitError(
                "gate must contain 'target_qubit' as a key."
            )

        if "control_qubit" not in gate.keys():
            raise QuantestPyCircuitError(
                "gate must contain 'control_qubit' as a key."
            )

        if "control_value" not in gate.keys():
            raise QuantestPyCircuitError(
                "gate must contain 'control_value' as a key."
            )

        if not isinstance(gate["target_qubit"], list):
            raise QuantestPyCircuitError(
                'gate["target_qubit"] must be a list.'
            )

        if not isinstance(gate["control_qubit"], list):
            raise QuantestPyCircuitError(
                'gate["control_qubit"] must be a list.'
            )

        if not isinstance(gate["control_value"], list):
            raise QuantestPyCircuitError(
                'gate["control_value"] must be a list.'
            )

        if len(gate["control_qubit"]) != len(gate["control_value"]):
            raise QuantestPyCircuitError(
                "control_qubit and control_value must have the same length."
            )

        if len(gate["target_qubit"]) < 1:
            raise QuantestPyCircuitError(
                "'target_qubit' must not an empty list."
            )

        for qubit in gate["target_qubit"]:
            if not isinstance(qubit, int):
                raise QuantestPyCircuitError(
                    "Index in target_qubit must be integer type."
                )

            if qubit not in self._qubit_indices:
                raise QuantestPyCircuitError(
                    f"Index {qubit} in target_qubit out of range for "
                    f"circuit size {self._num_qubit}."
                )

        for qubit in gate["control_qubit"]:
            if not isinstance(qubit, int):
                raise QuantestPyCircuitError(
                    "Index in control_qubit must be integer type."
                )

            if qubit not in self._qubit_indices:
                raise QuantestPyCircuitError(
                    f"Index {qubit} in control_qubit out of range for "
                    f"circuit size {self._num_qubit}."
                )

        for value in gate["control_value"]:
            if not isinstance(value, int):
                raise QuantestPyCircuitError(
                    "Value in control_value must be integer type."
                )

            if value not in [0, 1]:
                raise QuantestPyCircuitError(
                    f"Value {value} in control_value is not acceptable. "
                    "It must be either 0 or 1."
                )

        if len(gate["target_qubit"]) != len(set(gate["target_qubit"])):
            raise QuantestPyCircuitError(
                "Duplicate in target_qubit is not supported."
            )

        if len(gate["control_qubit"]) != len(set(gate["control_qubit"])):
            raise QuantestPyCircuitError(
                "Duplicate in control_qubit is not supported."
            )

        if len(list(set(gate["target_qubit"]) & set(gate["control_qubit"]))) \
                > 0:
            raise QuantestPyCircuitError(
                f'target_qubit {gate["target_qubit"]} and '
                f'control_qubit {gate["control_qubit"]} have intersection.'
            )

        if gate["name"] in ["swap", "iswap"] and \
                len(gate["target_qubit"]) != 2:
            raise QuantestPyCircuitError(
                f'{gate["name"]} gate must have a list '
                "containing exactly 2 elements for 'target_qubit'."
            )

    def add_gate(self, gate: dict) -> None:
        self._diagnostic_gate(gate)
        self._gates.append(gate)

    def draw(self,):
        from quantestpy.visualization.quantestpy_circuit_drawer import \
            draw_circuit

        return draw_circuit(self)


if __name__ == "__main__":
    """Example showing how to use QuantestPyCircuit class."""

    circ = QuantestPyCircuit(3)
    circ.add_gate({"name": "x", "target_qubit": [0], "control_qubit": [],
                   "control_value": [], "parameter": []})
    circ.add_gate({"name": "x", "target_qubit": [2], "control_qubit": [0],
                   "control_value": [1], "parameter": []})
    circ.add_gate({"name": "h", "target_qubit": [0], "control_qubit": [],
                   "control_value": [], "parameter": []})
