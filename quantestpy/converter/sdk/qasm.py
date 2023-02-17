from quantestpy import QuantestPyCircuit
from quantestpy.converter.sdk.qiskit import _cvt_qiskit_to_quantestpy_circuit
from quantestpy.exceptions import QuantestPyError

try:
    from qiskit import QuantumCircuit

except ModuleNotFoundError:
    def _cvt_openqasm_to_quantestpy_circuit(qasm: str) -> QuantestPyCircuit:
        raise QuantestPyError(
            "Qiskit is missing. Please install it."
        )
else:
    def _cvt_openqasm_to_quantestpy_circuit(qasm: str) -> QuantestPyCircuit:
        qiskit_circuit = QuantumCircuit.from_qasm_str(qasm)
        return _cvt_qiskit_to_quantestpy_circuit(qiskit_circuit)
