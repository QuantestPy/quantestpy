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

    def __init__(self, num_qubit: int):
        self._gates = []
        self._qubits = [0 for _ in range(num_qubit)]
        self._num_qubit = num_qubit

    def add_gate(self, gate: dict) -> None:
        """
        Example
        gate = {"name": "x", "target_qubit": 1, "control_qubit": 0}
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

        if gate["name"] not in _IMPLEMENTED_GATES:
            raise QuantestPyTestCircuitError(
                f'{gate["name"]} is not implemented.'
                f'Implemented gates: {_IMPLEMENTED_GATES}'
            )

        if not isinstance(gate["target_qubit"], int):
            raise QuantestPyTestCircuitError(
                'gate["target_qubit"]s type must be integer'
            )

        if gate["name"] in ["cx", "cnot"] \
                and "control_qubit" not in gate.keys():
            raise QuantestPyTestCircuitError(
                "gate must contain 'control_qubit' as a key "
                f'when using {gate["name"]}.'
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

    def _create_all_qubit_op_from_single_qubit_op(
            self, single_qubit_op: np.ndarray, target: int) -> np.ndarray:

        for qubit_id in range(self._num_qubit):
            if qubit_id == 0:
                if qubit_id == target:
                    all_qubit_op = single_qubit_op
                else:
                    all_qubit_op = _ID

            else:
                if qubit_id == target:
                    all_qubit_op = self._calculate_matrix_tensor_prod(
                        all_qubit_op, single_qubit_op)
                else:
                    all_qubit_op = self._calculate_matrix_tensor_prod(
                        all_qubit_op, _ID)

        return all_qubit_op

    def _get_state_vector(self,) -> np.ndarray:

        # initialize state vector
        state_vec = [1.+0j, 0.+0j]
        state_vec += [0 for _ in range(2**self._num_qubit-2)]
        state_vec = np.array(state_vec)

        # initialize circuit operator
        self._circuit_op = np.eye(2**self._num_qubit)

        # apply each gate to state vector
        for gate in self._gates:
            if gate["name"] == "x":
                all_qubit_op = self._create_all_qubit_op_from_single_qubit_op(
                    _X, gate["target_qubit"])

            elif gate["name"] == "h":
                all_qubit_op = self._create_all_qubit_op_from_single_qubit_op(
                    _H, gate["target_qubit"])

            elif gate["name"] == "s":
                all_qubit_op = self._create_all_qubit_op_from_single_qubit_op(
                    _S, gate["target_qubit"])

            elif gate["name"] == "t":
                all_qubit_op = self._create_all_qubit_op_from_single_qubit_op(
                    _T, gate["target_qubit"])

            elif gate["name"] == "cx" or gate["name"] == "cnot":
                trans = dict()
                for i in range(2**self._num_qubit):
                    i_bin = bin(i)[2:].zfill(self._num_qubit)
                    i_bin = list(i_bin)
                    if i_bin[gate["control_qubit"]] == "1":
                        if i_bin[gate["target_qubit"]] == "1":
                            i_bin[gate["target_qubit"]] = "0"
                        elif i_bin[gate["target_qubit"]] == "0":
                            i_bin[gate["target_qubit"]] = "1"
                        else:
                            raise

                    j_bin = "".join(i_bin)
                    j = int(j_bin, 2)
                    trans[i] = j

                all_qubit_op = np.zeros(
                    (2**self._num_qubit, 2**self._num_qubit))
                for i in range(2**self._num_qubit):
                    all_qubit_op[trans[i], i] = 1.

            else:
                raise

            state_vec = np.matmul(all_qubit_op, state_vec)
            self._circuit_op = np.matmul(self._circuit_op, all_qubit_op)

        return state_vec


    def _cvt_openqasm_to_test_circuit(self, qasm: str) -> TestCircuit:
        """Needs implemantation"""
        return "Not implemented yet..."


if __name__ == "__main__":
    """Example showing how to use TestCircuit class."""

    test_circ = TestCircuit(3)
    test_circ.add_gate({"name": "x", "target_qubit": 0})
    test_circ.add_gate({"name": "cx", "target_qubit": 2, "control_qubit": 0})
    test_circ.add_gate({"name": "h", "target_qubit": 0})

    state_vector = test_circ._get_state_vector()
