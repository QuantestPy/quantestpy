from typing import Union

from quantestpy import QuantestPyCircuit
from quantestpy.exceptions import QuantestPyError

try:
    from quri_parts.circuit import (ImmutableBoundParametricQuantumCircuit,
                                    NonParametricQuantumCircuit)

except ModuleNotFoundError:
    def _is_instance_of_quri_parts_quantumcircuit(circuit) -> bool:
        # pylint: disable=unused-argument
        # since package quri_parts does not exists,
        # input circuit is always not related to quri_parts.
        return False

    def _cvt_quri_parts_circuit_to_quantestpy_circuit(quri_parts_circuit
                                                      ) -> QuantestPyCircuit:
        raise QuantestPyError(
            "QURI Parts is missing. Please install it."
        )

else:
    def _cvt_quri_parts_circuit_to_quantestpy_circuit(
        quri_parts_circuit: Union[
            NonParametricQuantumCircuit,
            ImmutableBoundParametricQuantumCircuit
            ]) -> QuantestPyCircuit:
        num_qubits = quri_parts_circuit.qubit_count
        circuit = QuantestPyCircuit(num_qubits)
        for gate in quri_parts_circuit.gates:

            name: str
            target_qubit = list(gate.target_indices)
            control_qubit = list(gate.control_indices)
            control_value = [1 for _ in range(len(control_qubit))]
            parameter = list(gate.params)

            # quri_parts.circuit.SingleQubitGateNameType
            if gate.name == "Identity":
                name = "id"
            elif gate.name == "X":
                name = "x"
            elif gate.name == "Y":
                name = "y"
            elif gate.name == "Z":
                name = "z"
            elif gate.name == "H":
                name = "h"
            elif gate.name == "S":
                name = "s"
            elif gate.name == "Sdag":
                name = "sdg"
            elif gate.name == "SqrtX":
                name = "sx"
            elif gate.name == "SqrtXdag":
                name = "sxdg"
            elif gate.name == "T":
                name = "t"
            elif gate.name == "Tdag":
                name = "tdg"
            elif gate.name == "RX":
                name = "rx"
            elif gate.name == "RY":
                name = "ry"
            elif gate.name == "RZ":
                name = "rz"
            elif gate.name == "U3":
                name = "u"
                # set global phase as 0.
                parameter.append(0)
            # quri_parts.circuit.TwoQubitGateNameType
            elif gate.name == "CNOT":
                name = "x"
            elif gate.name == "CZ":
                name = "z"
            elif gate.name == "SWAP":
                name = "swap"
            else:
                # SqrtY, SqrtYdag, U1, U2, U3
                raise QuantestPyError(
                    f'QURI-Parts gate [{gate.name}] '
                    "is not supported in QuantestPy.\n"
                )

            circuit.add_gate(
                dict(name=name,
                     target_qubit=target_qubit,
                     control_qubit=control_qubit,
                     control_value=control_value,
                     parameter=parameter)
            )

        return circuit

    def _is_instance_of_quri_parts_quantumcircuit(circuit) -> bool:
        return (isinstance(circuit, NonParametricQuantumCircuit) or
                isinstance(circuit, ImmutableBoundParametricQuantumCircuit))
