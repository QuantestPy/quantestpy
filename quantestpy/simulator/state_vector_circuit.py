import itertools

import numpy as np

from quantestpy.simulator.exceptions import StateVectorCircuitError
from quantestpy.simulator.quantestpy_circuit import QuantestPyCircuit

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
_SX = np.array([[1+1j, 1-1j], [1-1j, 1+1j]])/2.
_SXdg = np.array([[1-1j, 1+1j], [1+1j, 1-1j]])/2.


def _u(parameter: list) -> np.ndarray:
    theta, phi, lambda_, gamma = parameter
    return np.array([
        [np.cos(theta/2), -np.exp(1j*lambda_) * np.sin(theta/2)],
        [np.exp(1j*phi)*np.sin(theta/2),
            np.exp(1j*(lambda_ + phi))*np.cos(theta/2)]])*np.exp(1j*gamma)


def _p(parameter: list) -> np.ndarray:
    lambda_ = parameter[0]
    return _u([0, 0, lambda_, 0])


def _rx(parameter: list) -> np.ndarray:
    theta = parameter[0]
    return _u([theta, -np.pi/2, np.pi/2, 0])


def _ry(parameter: list) -> np.ndarray:
    theta = parameter[0]
    return _u([theta, 0, 0, 0])


def _rz(parameter: list) -> np.ndarray:
    phi = parameter[0]
    return _p(parameter)*np.exp(-1j*phi/2)


def _r(parameter: list) -> np.ndarray:
    theta, phi = parameter
    return np.array([
        [np.cos(theta/2), -1j * np.exp(-1j*phi) * np.sin(theta/2)],
        [-1j * np.exp(1j*phi) * np.sin(theta/2), np.cos(theta/2)]
    ])


def _scalar(parameter: list) -> np.ndarray:
    theta = parameter[0]
    return _ID * np.exp(1j*theta)


# gates lists
_IMPLEMENTED_GATES_WITHOUT_PARAM = ["id", "x", "y", "z", "h", "s", "sdg",
                                    "t", "tdg", "swap", "iswap", "sx", "sxdg"]
_IMPLEMENTED_GATES_WITH_ONE_PARAM = ["rx", "ry", "rz", "p", "scalar"]
_IMPLEMENTED_GATES_WITH_TWO_PARAM = ["r"]
_IMPLEMENTED_GATES_WITH_FOUR_PARAM = ["u"]
_IMPLEMENTED_GATES_WITH_PARAM = _IMPLEMENTED_GATES_WITH_ONE_PARAM \
    + _IMPLEMENTED_GATES_WITH_TWO_PARAM + _IMPLEMENTED_GATES_WITH_FOUR_PARAM
_IMPLEMENTED_GATES = _IMPLEMENTED_GATES_WITHOUT_PARAM \
    + _IMPLEMENTED_GATES_WITH_PARAM


class StateVectorCircuit(QuantestPyCircuit):
    """
    This circuit class will be used inside the assert methods which deal with
    state vectors.
    """

    def __init__(self, num_qubit: int):
        super().__init__(num_qubit=num_qubit)
        self._from_right_to_left_for_qubit_ids = False
        self._binary_to_vector = None
        self._initial_state_vector = None

    def _diagnostic_gate(self, gate: dict) -> None:
        """Override"""
        super()._diagnostic_gate(gate)

        if "parameter" not in gate.keys():
            raise StateVectorCircuitError(
                "gate must contain 'parameter' as a key."
            )

        if gate["name"] not in _IMPLEMENTED_GATES:
            raise StateVectorCircuitError(
                f'{gate["name"]} is not implemented.'
                f'Implemented gates: {_IMPLEMENTED_GATES}'
            )

        if gate["name"] in _IMPLEMENTED_GATES_WITHOUT_PARAM and \
                len(gate["parameter"]) != 0:
            raise StateVectorCircuitError(
                f'{gate["name"]} gate must have an empty list for '
                "'parameter'."
            )

        if gate["name"] in _IMPLEMENTED_GATES_WITH_ONE_PARAM and \
                len(gate["parameter"]) != 1:
            raise StateVectorCircuitError(
                f'{gate["name"]} gate must have a list containing '
                "exactly 1 element for 'parameter'."
            )

        if gate["name"] in _IMPLEMENTED_GATES_WITH_TWO_PARAM and \
                len(gate["parameter"]) != 2:
            raise StateVectorCircuitError(
                f'{gate["name"]} gate must have a list containing '
                "exactly 2 elements for 'parameter'."
            )

        if gate["name"] in _IMPLEMENTED_GATES_WITH_FOUR_PARAM and \
                len(gate["parameter"]) != 4:
            raise StateVectorCircuitError(
                f'{gate["name"]} gate must have a list containing '
                "exactly 4 elements for 'parameter'."
            )

        if gate["name"] in _IMPLEMENTED_GATES_WITH_PARAM:
            for param in gate["parameter"]:
                if not isinstance(param, float) and not isinstance(param, int):
                    raise StateVectorCircuitError(
                        f'Parameter(s) in {gate["name"]} gate must be '
                        'float or integer type.'
                    )

    def _create_all_qubit_gate_from_original_qubit_gate(
            self,
            gate: np.ndarray,
            control_qubit: list,
            target_qubit: list,
            control_value: list) -> np.ndarray:

        all_qubit_gate = np.zeros((2**self._num_qubit, 2**self._num_qubit))
        bit_patterns_for_control_qubit = list(
            itertools.product([0, 1], repeat=len(control_qubit)))
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
            raise StateVectorCircuitError(
                'type of initial state vector must be numpy.ndarray.'
            )

        if initial_state_vector.shape != (2**self._num_qubit,):
            raise StateVectorCircuitError(
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
            if gate["name"] == "swap":
                all_qubit_gate1 = \
                    self._create_all_qubit_gate_from_original_qubit_gate(
                        _X,
                        gate["target_qubit"][1:],
                        gate["target_qubit"][:1],
                        [1]
                    )
                all_qubit_gate2 = \
                    self._create_all_qubit_gate_from_original_qubit_gate(
                        _X,
                        gate["control_qubit"] + gate["target_qubit"][:1],
                        gate["target_qubit"][1:],
                        gate["control_value"] + [1]
                    )
                whole_gates = np.matmul(all_qubit_gate1, whole_gates)
                whole_gates = np.matmul(all_qubit_gate2, whole_gates)
                whole_gates = np.matmul(all_qubit_gate1, whole_gates)
            elif gate["name"] == "iswap":
                all_qubit_gate1 = \
                    self._create_all_qubit_gate_from_original_qubit_gate(
                        _S,
                        gate["control_qubit"],
                        gate["target_qubit"][:1],
                        gate["control_value"]
                    )
                all_qubit_gate2 = \
                    self._create_all_qubit_gate_from_original_qubit_gate(
                        _S,
                        gate["control_qubit"],
                        gate["target_qubit"][1:],
                        gate["control_value"]
                    )
                all_qubit_gate3 = \
                    self._create_all_qubit_gate_from_original_qubit_gate(
                        _H,
                        gate["control_qubit"],
                        gate["target_qubit"][:1],
                        gate["control_value"]
                    )
                all_qubit_gate4 = \
                    self._create_all_qubit_gate_from_original_qubit_gate(
                        _X,
                        gate["control_qubit"] + gate["target_qubit"][:1],
                        gate["target_qubit"][1:],
                        gate["control_value"] + [1]
                    )
                all_qubit_gate5 = \
                    self._create_all_qubit_gate_from_original_qubit_gate(
                        _X,
                        gate["control_qubit"] + gate["target_qubit"][1:],
                        gate["target_qubit"][:1],
                        gate["control_value"] + [1]
                    )
                all_qubit_gate6 = \
                    self._create_all_qubit_gate_from_original_qubit_gate(
                        _H,
                        gate["control_qubit"],
                        gate["target_qubit"][1:],
                        gate["control_value"]
                    )
                whole_gates = np.matmul(all_qubit_gate1, whole_gates)
                whole_gates = np.matmul(all_qubit_gate2, whole_gates)
                whole_gates = np.matmul(all_qubit_gate3, whole_gates)
                whole_gates = np.matmul(all_qubit_gate4, whole_gates)
                whole_gates = np.matmul(all_qubit_gate5, whole_gates)
                whole_gates = np.matmul(all_qubit_gate6, whole_gates)
            else:
                if gate["name"] in ("id", "x", "y", "z", "h", "s", "t", "sx"):
                    original_qubit_gate = eval("_" + gate["name"].upper())
                elif gate["name"] in ("sdg", "tdg", "sxdg"):
                    original_qubit_gate = \
                        eval("_" + gate["name"][:-2].upper() + "dg")
                elif gate["name"] in (
                        "rx", "ry", "rz", "r", "u", "p", "scalar"):
                    original_qubit_gate = eval("_" + gate["name"]
                                               + '(gate["parameter"])')
                else:
                    raise StateVectorCircuitError(
                        "Unexpected error. Please report."
                    )
                all_qubit_gate = \
                    self._create_all_qubit_gate_from_original_qubit_gate(
                        original_qubit_gate,
                        gate["control_qubit"],
                        gate["target_qubit"],
                        gate["control_value"]
                    )
                whole_gates = np.matmul(all_qubit_gate, whole_gates)

        return whole_gates

    def draw(self,):
        from quantestpy.visualization.state_vector_circuit_drawer import \
            draw_circuit

        return draw_circuit(self)


def cvt_quantestpy_circuit_to_state_vector_circuit(
        qc: QuantestPyCircuit) -> StateVectorCircuit:
    """Converts an instance of QuantestPyCircuit to that of StateVectorCircuit.
    """
    if not isinstance(qc, QuantestPyCircuit):
        raise StateVectorCircuitError(
            "Input circuit must be an instance of QuantestPyCircuit."
        )

    svc = StateVectorCircuit(num_qubit=qc.num_qubit)
    for gate in qc.gates:
        svc.add_gate(gate)

    return svc


if __name__ == "__main__":
    """Example showing how to use TestCircuit class."""

    circ = StateVectorCircuit(3)
    circ.add_gate({"name": "x", "target_qubit": [0], "control_qubit": [],
                   "control_value": [], "parameter": []})
    circ.add_gate(
        {"name": "x", "target_qubit": [2], "control_qubit": [0],
         "control_value": [1], "parameter": []})
    circ.add_gate({"name": "h", "target_qubit": [0], "control_qubit": [],
                   "control_value": [], "parameter": []})

    state_vector = circ._get_state_vector()
