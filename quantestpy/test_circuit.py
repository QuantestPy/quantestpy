import numpy as np
from quantestpy.exceptions import QuantestPyTestCircuitError

# inside of test unit

_ID = np.array([[1, 0], [0, 1]])
_X = np.array([[0, 1], [1, 0]])
_H = np.array([[1, 1], [1, -1]])/np.sqrt(2.)
_S = np.array([[1, 0], [0, 1j]])
_T = np.array([[1, 0], [0, np.exp(1j*np.pi/4)]])
_IMPLEMENTED_GATES = ["x", "h", "s", "t", "cx", "cnot"]


class TestCircuit:
    """
    This circuit class will be always used as an input to assert methods
    which deal with circuits. Mathematical operations such as applying gates
    will be executed using the methods of this class.
    """

    def __init__(self,
                 num_qubit: int,
                 from_right_to_left_for_qubit_ids: bool = False):
        self._gates = []
        self._qubits = [0 for _ in range(num_qubit)]
        self._num_qubit = num_qubit
        self._from_right_to_left_for_qubit_ids = \
            from_right_to_left_for_qubit_ids
        self._binary_to_vector = None

    def add_gate(self, gate: dict) -> None:
        """
        Example
        gate = {"name": "x", "target_qubit": [1], "control_qubit": []}
        gate = {"name": "cx", "target_qubit": [1], "control_qubit": [0]}
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

        self._gates.append(gate)

    @staticmethod
    def _calculate_matrix_tensor_prod(mat1: np.ndarray, mat2: np.ndarray) \
            -> np.ndarray:
        m, n = mat1.shape
        for i in range(m):  # loop in row
            for j in range(n):  # loop in column
                c = mat1[i, j] * mat2
                if j == 0:
                    column = c
                else:
                    column = np.append(column, c, axis=1)

            if i == 0:
                row = column
            else:
                row = np.append(row, column, axis=0)

        if row.shape[0] != m * mat2.shape[0]:
            raise

        if row.shape[1] != n * mat2.shape[1]:
            raise

        return row

    def _create_all_qubit_gate_from_single_qubit_gate(
            self, single_qubit_gate: np.ndarray, target: int) -> np.ndarray:

        for qubit_id in range(self._num_qubit):
            if qubit_id == 0:
                if qubit_id == target:
                    all_qubit_gate = single_qubit_gate
                else:
                    all_qubit_gate = _ID

            else:
                if qubit_id == target:
                    if self._from_right_to_left_for_qubit_ids:
                        all_qubit_gate = self._calculate_matrix_tensor_prod(
                            single_qubit_gate, all_qubit_gate)

                    else:
                        all_qubit_gate = self._calculate_matrix_tensor_prod(
                            all_qubit_gate, single_qubit_gate)

                else:
                    if self._from_right_to_left_for_qubit_ids:
                        all_qubit_gate = self._calculate_matrix_tensor_prod(
                            _ID, all_qubit_gate)

                    else:
                        all_qubit_gate = self._calculate_matrix_tensor_prod(
                            all_qubit_gate, _ID)

        return all_qubit_gate

    def _create_all_qubit_gate_from_cnot_gate(
            self, control: int, target: int) -> np.ndarray:

        if self._binary_to_vector is None:
            self._binary_to_vector = {}
            for i in range(2**self._num_qubit):
                i_binary = bin(i)[2:].zfill(self._num_qubit)

                if self._from_right_to_left_for_qubit_ids:
                    i_binary = "".join(list(reversed(i_binary)))

                i_vector = np.zeros(2**self._num_qubit)
                i_vector[i] = 1.
                self._binary_to_vector[i_binary] = i_vector

        all_qubit_gate = np.zeros(
            (2**self._num_qubit, 2**self._num_qubit))

        for binary_before_cnot in self._binary_to_vector.keys():

            binary_tmp = list(binary_before_cnot)
            if binary_tmp[control] == "1":
                if binary_tmp[target] == "1":
                    binary_tmp[target] = "0"
                elif binary_tmp[target] == "0":
                    binary_tmp[target] = "1"
                else:
                    raise

            binary_after_cnot = "".join(binary_tmp)

            vector_after_cnot = self._binary_to_vector[binary_after_cnot]
            vector_before_cnot = self._binary_to_vector[binary_before_cnot]
            all_qubit_gate += \
                vector_after_cnot.reshape(-1, 1) * vector_before_cnot

        return all_qubit_gate

    def _get_state_vector(self,) -> np.ndarray:

        # initialize state vector
        state_vec = [1.+0j, 0.+0j]
        state_vec += [0 for _ in range(2**self._num_qubit-2)]
        state_vec = np.array(state_vec)

        whole_gates = self._get_circuit_operator()
        state_vec = np.matmul(whole_gates, state_vec)

        return state_vec

    def _get_circuit_operator(self,) -> np.ndarray:

        # initialize circuit operator
        whole_gates = np.eye(2**self._num_qubit)

        # apply each gate to state vector
        for gate in self._gates:
            if gate["name"] == "x":
                all_qubit_gate = \
                    self._create_all_qubit_gate_from_single_qubit_gate(
                        _X, gate["target_qubit"][0])

            elif gate["name"] == "h":
                all_qubit_gate = \
                    self._create_all_qubit_gate_from_single_qubit_gate(
                        _H, gate["target_qubit"][0])

            elif gate["name"] == "s":
                all_qubit_gate = \
                    self._create_all_qubit_gate_from_single_qubit_gate(
                        _S, gate["target_qubit"][0])

            elif gate["name"] == "t":
                all_qubit_gate = \
                    self._create_all_qubit_gate_from_single_qubit_gate(
                        _T, gate["target_qubit"][0])

            elif gate["name"] == "cx" or gate["name"] == "cnot":
                all_qubit_gate = \
                    self._create_all_qubit_gate_from_cnot_gate(
                        gate["control_qubit"][0], gate["target_qubit"][0])

            else:
                raise

            whole_gates = np.matmul(all_qubit_gate, whole_gates)

        return whole_gates


def cvt_openqasm_to_test_circuit(qasm: str) -> TestCircuit:
    """Needs implemantation"""
    return "Not implemented yet..."


if __name__ == "__main__":
    """Example showing how to use TestCircuit class."""

    test_circ = TestCircuit(3)
    test_circ.add_gate({"name": "x", "target_qubit": [0], "control_qubit": []})
    test_circ.add_gate(
        {"name": "cx", "target_qubit": [2], "control_qubit": [0]})
    test_circ.add_gate({"name": "h", "target_qubit": [0], "control_qubit": []})

    state_vector = test_circ._get_state_vector()
