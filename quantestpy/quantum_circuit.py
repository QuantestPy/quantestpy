import numpy as np
import qiskit
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.quantum_info.operators import Operator
from typing import Union

from quantestpy import matrix


def assert_equal_to_operator(
        qasm: str,
        operator: Union[
            np.ndarray,
            np.matrix,
            qiskit.quantum_info.operators.operator.Operator],
        number_of_decimal_places: int = 5,
        check_including_global_phase: bool = True,
        msg=None) -> None:

    # check type
    if not isinstance(qasm, str):
        raise TypeError("The type of qasm must be string.")

    qc = QuantumCircuit.from_qasm_str(qasm)
    operator_from_qc = Operator(qc)

    matrix.assert_equal(
        operator_from_qc,
        operator,
        number_of_decimal_places,
        check_including_global_phase,
        msg)


"""
def assert_is_all_zero(
        qasm: str,
        number_of_decimal_places: int = 5,
        msg=None):

    # check type
    if not isinstance(qasm, str):
        raise TypeError("The type of qasm must be string.")

    # construct state vector from qasm
    qc = QuantumCircuit.from_qasm_str(qasm)
    state_vec = np.array(Statevector(qc))

    # remove global phase
    for i in range(len(state_vec)):
        if abs(state_vec[i]) > 0.:
            a_global_phase = state_vec[i] / abs(state_vec[i])
            break

    state_vec = state_vec * a_global_phase.conj()
"""
