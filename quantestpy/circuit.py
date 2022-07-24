import numpy as np
import qiskit
from typing import Union

from quantestpy import matrix
from quantestpy import TestCircuit
from quantestpy.exceptions import QuantestPyError


def assert_equal_to_operator(
        operator: Union[
            np.ndarray,
            np.matrix,
            qiskit.quantum_info.operators.operator.Operator],
        qasm: str = None,
        test_circuit: TestCircuit = None,
        number_of_decimal_places: int = 5,
        check_including_global_phase: bool = True,
        msg=None) -> None:

    #
    if qasm is None and test_circuit is None:
        raise QuantestPyError(
            "Missing qasm or test circuit."
        )

    if qasm is not None and test_circuit is not None:
        raise QuantestPyError(
            "Qasm and test circuit must not both be given."
        )

    if qasm is not None:
        raise QuantestPyError(
            "Loading qasm is not yet implemented."
        )

    # check type
    # if not isinstance(qasm, str):
    #    raise TypeError("The type of qasm must be string.")

    _ = test_circuit._get_state_vector()
    operator_from_test_circuit = test_circuit._circuit_op

    matrix.assert_equal(
        operator_from_test_circuit,
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
