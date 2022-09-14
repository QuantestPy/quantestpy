import itertools

import numpy as np

from quantestpy.exceptions import QuantestPyTestCircuitError

# inside of test unit
# single qubit gates
_ID = np.array([[1, 0], [0, 1]])
_X = np.array([[0, 1], [1, 0]])
_Y = np.array([[0, -1j], [1j, 0]])
_Z = np.array([[1, 0], [0, -1]])
_H = np.array([[1, 1], [1, -1]])/np.sqrt(2.)
_S = np.array([[1, 0], [0, 1j]])
_Sdg = np.array([[1, 0], [0, -1j]])
_T = np.array([[1, 0], [0, np.exp(1j*np.pi/4)]])
_Tdg = np.array([[1, 0], [0, np.exp(-1j*np.pi/4)]])

# U gates


def _u3(parameter: list) -> np.ndarray:
    theta, phi, lambda_ = parameter
    return np.array([
        [np.cos(theta/2), -np.exp(1j*lambda_) * np.sin(theta/2)],
        [np.exp(1j*phi)*np.sin(theta/2),
         np.exp(1j*(lambda_ + phi))*np.cos(theta/2)]])


def _u2(parameter: list) -> np.ndarray:
    phi, lambda_ = parameter
    return _u3([np.pi/2, phi, lambda_])


def _u1(parameter: list) -> np.ndarray:
    lambda_ = parameter[0]
    return _u3([0, 0, lambda_])


# rotation gates
def _rx(parameter: list) -> np.ndarray:
    theta = parameter[0]
    return _u3([theta, -np.pi/2, np.pi/2])


def _ry(parameter: list) -> np.ndarray:
    theta = parameter[0]
    return _u3([theta, 0, 0])


def _rz(parameter: list) -> np.ndarray:
    phi = parameter[0]
    return _u1(parameter)*np.exp(-1j*phi/2)


# scalar gate
def _scalar(parameter: list) -> np.ndarray:
    theta = parameter[0]
    return _ID * np.exp(1j*theta)


# gates lists
_IMPLEMENTED_SINGLE_QUBIT_GATES_WITHOUT_PARAM = [
    "id", "x", "y", "z", "h", "s", "sdg", "t", "tdg"]
_IMPLEMENTED_SINGLE_QUBIT_GATES_WITH_PARAM = [
    "rx", "ry", "rz", "u1", "u2", "u3", "scalar"]
_IMPLEMENTED_MULTIPLE_QUBIT_GATES_WITHOUT_PARAM = ["cx", "cy", "cz", "ch"]
_IMPLEMENTED_MULTIPLE_QUBIT_GATES_WITH_PARAM = [
    "crx", "cry", "crz", "cu1", "cu3"]
_IMPLEMENTED_SINGLE_QUBIT_GATES = \
    _IMPLEMENTED_SINGLE_QUBIT_GATES_WITHOUT_PARAM \
    + _IMPLEMENTED_SINGLE_QUBIT_GATES_WITH_PARAM
_IMPLEMENTED_MULTIPLE_QUBIT_GATES = \
    _IMPLEMENTED_MULTIPLE_QUBIT_GATES_WITHOUT_PARAM \
    + _IMPLEMENTED_MULTIPLE_QUBIT_GATES_WITH_PARAM
_IMPLEMENTED_GATES_WITHOUT_PARAM = \
    _IMPLEMENTED_SINGLE_QUBIT_GATES_WITHOUT_PARAM \
    + _IMPLEMENTED_MULTIPLE_QUBIT_GATES_WITHOUT_PARAM
_IMPLEMENTED_GATES_WITH_ONE_PARAM = [
    "rx", "ry", "rz", "u1", "crx", "cry", "crz", "cu1", "scalar"]
_IMPLEMENTED_GATES_WITH_TWO_PARAM = ["u2"]
_IMPLEMENTED_GATES_WITH_THREE_PARAM = ["u3", "cu3"]
_IMPLEMENTED_GATES_WITH_PARAM = _IMPLEMENTED_SINGLE_QUBIT_GATES_WITH_PARAM \
    + _IMPLEMENTED_MULTIPLE_QUBIT_GATES_WITH_PARAM
_IMPLEMENTED_GATES = _IMPLEMENTED_SINGLE_QUBIT_GATES \
    + _IMPLEMENTED_MULTIPLE_QUBIT_GATES


class TestCircuit:
    """
    This circuit class will be always used as an input to assert methods
    which deal with circuits. Mathematical operations such as applying gates
    will be executed using the methods of this class.
    """

    def __init__(self, num_qubit: int):
        self._gates = []
        self._qubit_indices = [i for i in range(num_qubit)]
        self._num_qubit = num_qubit
        self._from_right_to_left_for_qubit_ids = False
        self._binary_to_vector = None
        self._initial_state_vector = None

    def add_gate(self, gate: dict) -> None:
        """
        Example
        gate = {"name": "x", "target_qubit": [1], "control_qubit": [],
                "control_value": [], "parameter": []}
        gate = {"name": "cx", "target_qubit": [1], "control_qubit": [0],
                "control_value": [1], "parameter": []}
        """
        if not isinstance(gate, dict):
            raise QuantestPyTestCircuitError(
                "gate's type must be dictionary which contains 'name', "
                "'target_qubit' and optionally 'control_qubit' as keys."
            )

        if "name" not in gate.keys():
            raise QuantestPyTestCircuitError(
                "gate must contain 'name' as a key."
            )

        if "target_qubit" not in gate.keys():
            raise QuantestPyTestCircuitError(
                "gate must contain 'target_qubit' as a key."
            )

        if "control_qubit" not in gate.keys():
            raise QuantestPyTestCircuitError(
                "gate must contain 'control_qubit' as a key."
            )

        if "control_value" not in gate.keys():
            raise QuantestPyTestCircuitError(
                "gate must contain 'control_value' as a key."
            )

        if "parameter" not in gate.keys():
            raise QuantestPyTestCircuitError(
                "gate must contain 'parameter' as a key."
            )

        if gate["name"] not in _IMPLEMENTED_GATES:
            raise QuantestPyTestCircuitError(
                f'{gate["name"]} is not implemented.'
                f'Implemented gates: {_IMPLEMENTED_GATES}'
            )

        if not isinstance(gate["target_qubit"], list):
            raise QuantestPyTestCircuitError(
                'gate["target_qubit"] must be a list'
            )

        if not isinstance(gate["control_qubit"], list):
            raise QuantestPyTestCircuitError(
                'gate["control_qubit"] must be a list'
            )

        if not isinstance(gate["control_value"], list):
            raise QuantestPyTestCircuitError(
                'gate["control_value"] must be a list'
            )

        if len(gate["control_qubit"]) != len(gate["control_value"]):
            raise QuantestPyTestCircuitError(
                "control_qubit and control_value must have the same lenght."
            )

        if len(gate["target_qubit"]) < 1:
            raise QuantestPyTestCircuitError(
                "'target_qubit' must not an empty list."
            )

        if gate["name"] in _IMPLEMENTED_SINGLE_QUBIT_GATES and \
                len(gate["control_qubit"]) != 0:
            raise QuantestPyTestCircuitError(
                "single qubit gate must have an empty list for "
                "'control_qubit'."
            )

        if gate["name"] in _IMPLEMENTED_SINGLE_QUBIT_GATES and \
                len(gate["control_value"]) != 0:
            raise QuantestPyTestCircuitError(
                "single qubit gate must have an empty list for "
                "'control_value'."
            )

        if gate["name"] == "cx" and len(gate["control_qubit"]) < 1:
            raise QuantestPyTestCircuitError(
                "cx gate must not have an empty list for "
                "'control_qubit' and 'control_value'."
            )

        for qubit in gate["target_qubit"]:
            if not isinstance(qubit, int):
                raise QuantestPyTestCircuitError(
                    "Index in target_qubit must be integer type."
                )

            if qubit not in self._qubit_indices:
                raise QuantestPyTestCircuitError(
                    f"Index {qubit} in target_qubit out of range for "
                    f"test_circuit size {self._num_qubit}."
                )

        for qubit in gate["control_qubit"]:
            if not isinstance(qubit, int):
                raise QuantestPyTestCircuitError(
                    "Index in control_qubit must be integer type."
                )

            if qubit not in self._qubit_indices:
                raise QuantestPyTestCircuitError(
                    f"Index {qubit} in control_qubit out of range for "
                    f"test_circuit size {self._num_qubit}."
                )

        for value in gate["control_value"]:
            if not isinstance(value, int):
                raise QuantestPyTestCircuitError(
                    "Value in control_value must be integer type."
                )

            if value not in [0, 1]:
                raise QuantestPyTestCircuitError(
                    f"Value {value} in control_value is not acceptable. "
                    f"It must be either 0 or 1."
                )

        if len(gate["target_qubit"]) != len(set(gate["target_qubit"])):
            raise QuantestPyTestCircuitError(
                "Duplicate in target_qubit is not supported."
            )

        if len(gate["control_qubit"]) != len(set(gate["control_qubit"])):
            raise QuantestPyTestCircuitError(
                "Duplicate in control_qubit is not supported."
            )

        if len(list(set(gate["target_qubit"]) & set(gate["control_qubit"]))) \
                > 0:
            raise QuantestPyTestCircuitError(
                f'target_qubit {gate["target_qubit"]} and '
                f'control_qubit {gate["control_qubit"]} have intersection.'
            )

        if gate["name"] in _IMPLEMENTED_GATES_WITHOUT_PARAM and \
                len(gate["parameter"]) != 0:
            raise QuantestPyTestCircuitError(
                "Gates with no parameters must have an empty list for "
                "'parameter'."
            )

        if gate["name"] in _IMPLEMENTED_GATES_WITH_ONE_PARAM and \
                len(gate["parameter"]) != 1:
            raise QuantestPyTestCircuitError(
                "Gates with one parameters must have a list containing "
                "exactly 1 element for 'parameter'."
            )

        if gate["name"] in _IMPLEMENTED_GATES_WITH_TWO_PARAM and \
                len(gate["parameter"]) != 2:
            raise QuantestPyTestCircuitError(
                "Gates with two parameters must have a list containing "
                "exactly 2 elements for 'parameter'."
            )

        if gate["name"] in _IMPLEMENTED_GATES_WITH_THREE_PARAM and \
                len(gate["parameter"]) != 3:
            raise QuantestPyTestCircuitError(
                "Gates with three parameters must have a list containing "
                "exactly 3 elements for 'parameter'."
            )
        if gate["name"] in _IMPLEMENTED_GATES_WITH_PARAM:
            for param in gate["parameter"]:
                if not isinstance(param, float) and not isinstance(param, int):
                    raise QuantestPyTestCircuitError(
                        "Parameters must be float or integer type.")

        self._gates.append(gate)

    def _create_all_qubit_gate_from_original_qubit_gate(
            self,
            gate: np.ndarray,
            control_qubit: list,
            target_qubit: list,
            control_value: list) -> np.ndarray:

        all_qubit_gate = np.zeros((2**self._num_qubit, 2**self._num_qubit))
        bit_patterns_for_control_qubit = \
            list(itertools.product([0, 1], repeat=len(control_qubit)))
        for bit_pattern in bit_patterns_for_control_qubit:
            term = 1
            for i in range(self._num_qubit):
                if i in control_qubit:
                    if bit_pattern[control_qubit.index(i)] == 0:
                        # |0><0|
                        if self._from_right_to_left_for_qubit_ids:
                            term = np.kron(np.array([[1, 0], [0, 0]]), term)
                        else:
                            term = np.kron(term, np.array([[1, 0], [0, 0]]))
                    else:
                        # |1><1|
                        if self._from_right_to_left_for_qubit_ids:
                            term = np.kron(np.array([[0, 0], [0, 1]]), term)
                        else:
                            term = np.kron(term, np.array([[0, 0], [0, 1]]))
                elif i in target_qubit:
                    if list(bit_pattern) == control_value:
                        if self._from_right_to_left_for_qubit_ids:
                            term = np.kron(gate, term)
                        else:
                            term = np.kron(term, gate)
                    else:
                        if self._from_right_to_left_for_qubit_ids:
                            term = np.kron(_ID, term)
                        else:
                            term = np.kron(term, _ID)
                else:
                    if self._from_right_to_left_for_qubit_ids:
                        term = np.kron(_ID, term)
                    else:
                        term = np.kron(term, _ID)
            all_qubit_gate = all_qubit_gate + term

        return all_qubit_gate

    def set_initial_state_vector(self, initial_state_vector: np.ndarray) \
            -> None:

        if not isinstance(initial_state_vector, np.ndarray):
            raise QuantestPyTestCircuitError(
                'type of initial state vector must be numpy.ndarray.'
            )

        if initial_state_vector.shape != (2**self._num_qubit,):
            raise QuantestPyTestCircuitError(
                "shape of initial state vector is invalid. It must be "
                "(2**num_qubit,)."
            )

        self._initial_state_vector = initial_state_vector

    def _get_state_vector(self,) -> np.ndarray:

        # initialize state vector if not given
        if self._initial_state_vector is None:
            state_vec = [1.+0j, 0.+0j]
            state_vec += [0 for _ in range(2**self._num_qubit-2)]
            self._initial_state_vector = np.array(state_vec)

        whole_gates = self._get_whole_gates()
        state_vec = np.matmul(whole_gates, self._initial_state_vector)

        return state_vec

    def _get_whole_gates(self,) -> np.ndarray:

        # initialize circuit operator
        whole_gates = np.eye(2**self._num_qubit)

        # apply each gate to state vector
        for gate in self._gates:
            if gate["name"] == "id":
                original_qubit_gate = _ID
            elif gate["name"] in ("x", "cx"):
                original_qubit_gate = _X
            elif gate["name"] in ("y", "cy"):
                original_qubit_gate = _Y
            elif gate["name"] in ("z", "cz"):
                original_qubit_gate = _Z
            elif gate["name"] in ("h", "ch"):
                original_qubit_gate = _H
            elif gate["name"] == "s":
                original_qubit_gate = _S
            elif gate["name"] == "sdg":
                original_qubit_gate = _Sdg
            elif gate["name"] == "t":
                original_qubit_gate = _T
            elif gate["name"] == "tdg":
                original_qubit_gate = _Tdg
            elif gate["name"] in ("rx", "crx"):
                original_qubit_gate = _rx(gate["parameter"])
            elif gate["name"] in ("ry", "cry"):
                original_qubit_gate = _ry(gate["parameter"])
            elif gate["name"] in ("rz", "crz"):
                original_qubit_gate = _rz(gate["parameter"])
            elif gate["name"] in ("u1", "cu1"):
                original_qubit_gate = _u1(gate["parameter"])
            elif gate["name"] in ("u2", "cu2"):
                original_qubit_gate = _u2(gate["parameter"])
            elif gate["name"] in ("u3", "cu3"):
                original_qubit_gate = _u3(gate["parameter"])
            elif gate["name"] == "scalar":
                original_qubit_gate = _scalar(gate["parameter"])
            else:
                raise

            all_qubit_gate = \
                self._create_all_qubit_gate_from_original_qubit_gate(
                    original_qubit_gate, gate["control_qubit"],
                    gate["target_qubit"], gate["control_value"])

            whole_gates = np.matmul(all_qubit_gate, whole_gates)

        return whole_gates


if __name__ == "__main__":
    """Example showing how to use TestCircuit class."""

    test_circ = TestCircuit(3)
    test_circ.add_gate({"name": "x", "target_qubit": [0], "control_qubit": [],
                        "control_value": [], "parameter": []})
    test_circ.add_gate(
        {"name": "cx", "target_qubit": [2], "control_qubit": [0],
         "control_value": [1], "parameter": []})
    test_circ.add_gate({"name": "h", "target_qubit": [0], "control_qubit": [],
                        "control_value": [], "parameter": []})

    state_vector = test_circ._get_state_vector()
