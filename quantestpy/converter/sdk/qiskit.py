from quantestpy import QuantestPyCircuit
from quantestpy.exceptions import QuantestPyError

_IMPLEMENTED_QISKIT_GATES = [
    "ccx", "ccz", "ch", "cp", "crx", "cry", "crz", "cs", "csdg", "cswap",
    "csx", "cu", "cx", "cy", "cz", "h", "id", "iswap", "mcp", "mcx",
    "p", "r", "rx", "ry", "rz", "s", "sdg", "swap", "sx", "sxdg",
    "t", "tdg", "u", "x", "y", "z"
    ]

try:
    from qiskit import QuantumCircuit, assemble

except ModuleNotFoundError:
    def _is_instance_of_qiskit_quantumcircuit(circuit) -> bool:
        # pylint: disable=unused-argument
        # input circuit is not qiskit's quantum circuit
        # because qiskit does not exists.
        return False

    def _cvt_qiskit_to_quantestpy_circuit(qiskit_circuit) -> QuantestPyCircuit:
        raise QuantestPyError(
            "Qiskit is missing. Please install it."
        )

else:
    def _is_instance_of_qiskit_quantumcircuit(circuit) -> bool:
        return isinstance(circuit, QuantumCircuit)

    def _cvt_qiskit_to_quantestpy_circuit(qiskit_circuit) -> QuantestPyCircuit:

        qobj = assemble(qiskit_circuit)
        qobj_dict = qobj.to_dict()
        experiments = qobj_dict["experiments"][0]  # [0] changes list into dict
        gates = experiments["instructions"]
        num_qubits = experiments["config"]["n_qubits"]
        global_phase = experiments["header"]["global_phase"]
        circuit = QuantestPyCircuit(num_qubits)

        for gate in gates:
            # "ccx gate"
            if gate["name"] == "ccx":
                name = "x"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [1, 1]
                parameter = []
            elif gate["name"] == "ccx_o0":
                name = "x"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [0, 0]
                parameter = []
            elif gate["name"] == "ccx_o1":
                name = "x"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [1, 0]  # reverse order along with qubit order
                parameter = []
            elif gate["name"] == "ccx_o2":
                name = "x"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [0, 1]  # reverse order along with qubit order
                parameter = []

            # ccz gate
            elif gate["name"] == "ccz":
                name = "z"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [1, 1]
                parameter = []
            elif gate["name"] == "ccz_o0":
                name = "z"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [0, 0]
                parameter = []
            elif gate["name"] == "ccz_o1":
                name = "z"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [1, 0]  # reverse order along with qubit order
                parameter = []
            elif gate["name"] == "ccz_o2":
                name = "z"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [0, 1]  # reverse order along with qubit order
                parameter = []

            # ch gate
            elif gate["name"] == "ch":
                name = "h"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [1]
                parameter = []
            elif gate["name"] == "ch_o0":
                name = "h"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [0]
                parameter = []

            # cp gate
            elif gate["name"] == "cp":
                name = "p"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [1]
                parameter = gate["params"]
            elif gate["name"] == "cp_o0":
                name = "p"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [0]
                parameter = gate["params"]

            # crx gate
            elif gate["name"] == "crx":
                name = "rx"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [1]
                parameter = gate["params"]
            elif gate["name"] == "crx_o0":
                name = "rx"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [0]
                parameter = gate["params"]

            # cry gate
            elif gate["name"] == "cry":
                name = "ry"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [1]
                parameter = gate["params"]
            elif gate["name"] == "cry_o0":
                name = "ry"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [0]
                parameter = gate["params"]

            # crz gate
            elif gate["name"] == "crz":
                name = "rz"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [1]
                parameter = gate["params"]
            elif gate["name"] == "crz_o0":
                name = "rz"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [0]
                parameter = gate["params"]

            # cs gate
            elif gate["name"] == "cs":
                name = "s"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [1]
                parameter = []
            elif gate["name"] == "cs_o0":
                name = "s"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [0]
                parameter = []

            # csdg gate
            elif gate["name"] == "csdg":
                name = "sdg"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [1]
                parameter = []
            elif gate["name"] == "csdg_o0":
                name = "sdg"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [0]
                parameter = []

            # cswap gate
            elif gate["name"] == "cswap":
                name = "swap"
                target_qubit = gate["qubits"][-2:]
                control_qubit = gate["qubits"][:-2]
                control_value = [1]
                parameter = []
            elif gate["name"] == "cswap_o0":
                name = "swap"
                target_qubit = gate["qubits"][-2:]
                control_qubit = gate["qubits"][:-2]
                control_value = [0]
                parameter = []

            # csx gate
            elif gate["name"] == "csx":
                name = "sx"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [1]
                parameter = []
            elif gate["name"] == "csx_o0":
                name = "sx"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [0]
                parameter = []

            # cu gate
            elif gate["name"] == "cu":
                name = "u"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [1]
                parameter = gate["params"]
            elif gate["name"] == "cu_o0":
                name = "u"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [0]
                parameter = gate["params"]

            # cx gate
            elif gate["name"] == "cx":
                name = "x"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [1]
                parameter = []
            elif gate["name"] == "cx_o0":
                name = "x"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [0]
                parameter = []

            # cy gate
            elif gate["name"] == "cy":
                name = "y"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [1]
                parameter = []
            elif gate["name"] == "cy_o0":
                name = "y"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [0]
                parameter = []

            # cz gate
            elif gate["name"] == "cz":
                name = "z"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [1]
                parameter = []
            elif gate["name"] == "cz_o0":
                name = "z"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [0]
                parameter = []

            # h gate
            elif gate["name"] == "h":
                name = gate["name"]
                target_qubit = gate["qubits"][-1:]
                control_qubit = []
                control_value = []
                parameter = []

            # id gate
            elif gate["name"] == "id":
                name = "id"
                target_qubit = gate["qubits"][-1:]
                control_qubit = []
                control_value = []
                parameter = []

            # iswap gate
            elif gate["name"] == "iswap":
                name = gate["name"]
                target_qubit = gate["qubits"][-2:]
                control_qubit = []
                control_value = []
                parameter = []

            # mcp gate
            elif gate["name"] == "mcphase":
                name = "p"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [1]*len(control_qubit)
                parameter = gate["params"]

            # mcx gate
            elif gate["name"] == "mcx":
                name = "x"
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = [1]*len(control_qubit)
                parameter = []

            # p, r, rx, ry, rz gate
            elif gate["name"] in ["p", "r", "rx", "ry", "rz"]:
                name = gate["name"]
                target_qubit = gate["qubits"][-1:]
                control_qubit = []
                control_value = []
                parameter = gate["params"]

            # s, sdg gate
            elif gate["name"] in ["s", "sdg"]:
                name = gate["name"]
                target_qubit = gate["qubits"][-1:]
                control_qubit = []
                control_value = []
                parameter = []

            # swap gate
            elif gate["name"] == "swap":
                name = gate["name"]
                target_qubit = gate["qubits"][-2:]
                control_qubit = []
                control_value = []
                parameter = []

            # sx, sxdg, t, tdg gate
            elif gate["name"] in ["sx", "sxdg", "t", "tdg"]:
                name = gate["name"]
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = []
                parameter = []

            # u gate
            elif gate["name"] == "u":
                name = gate["name"]
                target_qubit = gate["qubits"][-1:]
                control_qubit = []
                control_value = []
                parameter = gate["params"]

            # x, y, z gate
            elif gate["name"] in ["x", "y", "z"]:
                name = gate["name"]
                target_qubit = gate["qubits"][-1:]
                control_qubit = gate["qubits"][:-1]
                control_value = []
                parameter = []

            # Other gates are not supported in QuantestPy
            else:
                raise QuantestPyError(
                    f'Qiskit gate [{gate["name"]}] '
                    "is not supported in QuantestPy.\n"
                    f'Implemented qiskit gates: {_IMPLEMENTED_QISKIT_GATES}'
                )

            # add gate
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
