from quantestpy import TestCircuit
from quantestpy.exceptions import QuantestPyError

try:
    from qiskit import QuantumCircuit, assemble
    qiskit_installed = True

except ModuleNotFoundError:
    qiskit_installed = False


def _cvt_qiskit_to_test_circuit(
        qiskit_circuit: QuantumCircuit) -> TestCircuit:

    if not qiskit_installed:
        raise QuantestPyError(
            "Qiskit is missing. Please install it."
        )

    qobj = assemble(qiskit_circuit)
    qobj_dict = qobj.to_dict()
    experiments = qobj_dict["experiments"][0]  # [0] changes list into dict.
    gates = experiments["instructions"]
    num_qubits = experiments["config"]["n_qubits"]
    global_phase = experiments["header"]["global_phase"]
    circuit = TestCircuit(num_qubits)

    # When num_qubits > 2, we must change the below for statement.
    for gate in gates:
        if "params" in gate:
            parameter = gate["params"]
        else:
            parameter = []

        if gate["name"] in ["cx", "cy", "cz", "ch",
                            "crx", "cry", "crz", "cu1", "cu3"]:
            control_value = [1]
        elif gate["name"] == "ccx":
            gate["name"] = "cx"
            control_value = [1, 1]
        else:
            control_value = []

        gate_test = dict(name=gate["name"],
                         target_qubit=[gate["qubits"][-1]],
                         control_qubit=gate["qubits"][:-1],
                         control_value=control_value,
                         parameter=parameter)
        circuit.add_gate(gate_test)

    if global_phase != 0.:
        gate_test = dict(name="scalar",
                         target_qubit=[0],
                         control_qubit=[],
                         control_value=[],
                         parameter=[global_phase])
        circuit.add_gate(gate_test)

    return circuit


def _cvt_openqasm_to_test_circuit(qasm: str) -> TestCircuit:

    if not qiskit_installed:
        raise QuantestPyError(
            "Qiskit is missing. Please install it."
        )

    qiskit_circuit = QuantumCircuit.from_qasm_str(qasm)
    return _cvt_qiskit_to_test_circuit(qiskit_circuit)
