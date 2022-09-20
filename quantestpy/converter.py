from quantestpy import TestCircuit
from quantestpy.exceptions import QuantestPyError

try:
    from qiskit import QuantumCircuit, assemble
    qiskit_installed = True

except ModuleNotFoundError:
    qiskit_installed = False


def _raise_error_if_not_qiskit_installed():

    if not qiskit_installed:
        raise QuantestPyError(
            "Qiskit is missing. Please install it."
        )


def _cvt_qiskit_to_test_circuit(qiskit_circuit) -> TestCircuit:

    _raise_error_if_not_qiskit_installed()

    qobj = assemble(qiskit_circuit)
    qobj_dict = qobj.to_dict()
    experiments = qobj_dict["experiments"][0]  # [0] changes list into dict.
    gates = experiments["instructions"]
    num_qubits = experiments["config"]["n_qubits"]
    global_phase = experiments["header"]["global_phase"]
    circuit = TestCircuit(num_qubits)

    for gate in gates:

        if "params" in gate:
            parameter = gate["params"]
        else:
            parameter = []

        if gate["name"] in ["swap", "cswap", "iswap"]:
            target_qubit = gate["qubits"][-2:]
            control_qubit = gate["qubits"][:-2]
        else:
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]

        if gate["name"] in ["cx", "cy", "cz", "ch",
                            "crx", "cry", "crz", "cswap"]:
            name = gate["name"][1:]
            control_value = [1]
        elif gate["name"] == "ccx":
            name = "x"
            control_value = [1, 1]
        elif gate["name"] in ["cp", "cu1"]:
            name = "p"
            control_value = [1]
        elif gate["name"] in ["cu", "cu3"]:
            name = "u"
            control_value = [1]
        elif gate["name"] == "u1":
            name = "p"
            control_value = []
        elif gate["name"] == "u3":
            name = "u"
            control_value = []
        else:
            name = gate["name"]
            control_value = []

        gate_test = dict(name=name,
                         target_qubit=target_qubit,
                         control_qubit=control_qubit,
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

    _raise_error_if_not_qiskit_installed()

    qiskit_circuit = QuantumCircuit.from_qasm_str(qasm)
    return _cvt_qiskit_to_test_circuit(qiskit_circuit)


def _is_instance_of_qiskit_quantumcircuit(circuit) -> bool:

    _raise_error_if_not_qiskit_installed()

    return isinstance(circuit, QuantumCircuit)
