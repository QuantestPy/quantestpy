from quantestpy import QuantestPyCircuit
from quantestpy.converter.sdk.qiskit import (
    _cvt_qiskit_to_quantestpy_circuit, _raise_error_if_not_qiskit_installed)

try:
    from qiskit import QuantumCircuit

except ModuleNotFoundError:
    pass


def _cvt_openqasm_to_quantestpy_circuit(qasm: str) -> QuantestPyCircuit:

    _raise_error_if_not_qiskit_installed()

    qiskit_circuit = QuantumCircuit.from_qasm_str(qasm)
    return _cvt_qiskit_to_quantestpy_circuit(qiskit_circuit)
