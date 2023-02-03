from quantestpy import QuantestPyCircuit
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


def _cvt_qiskit_to_quantestpy_circuit(qiskit_circuit) -> QuantestPyCircuit:

    _raise_error_if_not_qiskit_installed()

    qobj = assemble(qiskit_circuit)
    qobj_dict = qobj.to_dict()
    experiments = qobj_dict["experiments"][0]  # [0] changes list into dict.
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
        if gate["name"] == "ccx_o0":
            name = "x"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [0, 0]
            parameter = []
        if gate["name"] == "ccx_o1":
            name = "x"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [0, 1]
            parameter = []
        if gate["name"] == "ccx_o2":
            name = "x"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [1, 0]
            parameter = []

        # ccz gate
        if gate["name"] == "ccz":
            name = "z"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [1, 1]
            parameter = []
        if gate["name"] == "ccz_o0":
            name = "z"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [0, 0]
            parameter = []
        if gate["name"] == "ccz_o1":
            name = "z"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [0, 1]
            parameter = []
        if gate["name"] == "ccz_o2":
            name = "z"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [1, 0]
            parameter = []

        # ch gate
        if gate["name"] == "ch":
            name = "h"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [1]
            parameter = []
        if gate["name"] == "ch_o0":
            name = "h"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [0]
            parameter = []

        # cp gate
        if gate["name"] == "cp":
            name = "p"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [1]
            parameter = gate["params"]
        if gate["name"] == "cp_o0":
            name = "p"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [0]
            parameter = gate["params"]

        # crx gate
        if gate["name"] == "crx":
            name = "rx"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [1]
            parameter = gate["params"]
        if gate["name"] == "crx_o0":
            name = "rx"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [0]
            parameter = gate["params"]

        # cry gate
        if gate["name"] == "cry":
            name = "ry"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [1]
            parameter = gate["params"]
        if gate["name"] == "cry_o0":
            name = "ry"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [0]
            parameter = gate["params"]

        # crz gate
        if gate["name"] == "crz":
            name = "rz"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [1]
            parameter = gate["params"]
        if gate["name"] == "crz_o0":
            name = "rz"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [0]
            parameter = gate["params"]

        # cs gate
        if gate["name"] == "cs":
            name = "s"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [1]
            parameter = []
        if gate["name"] == "cs_o0":
            name = "s"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [0]
            parameter = []

        # csdg gate
        if gate["name"] == "csdg":
            name = "sdg"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [1]
            parameter = []
        if gate["name"] == "csdg_o0":
            name = "sdg"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [0]
            parameter = []

        # cswap gate
        if gate["name"] == "cswap":
            name = "swap"
            target_qubit = gate["qubits"][-2:]
            control_qubit = gate["qubits"][:-2]
            control_value = [1]
            parameter = []
        if gate["name"] == "cswap_o0":
            name = "swap"
            target_qubit = gate["qubits"][-2:]
            control_qubit = gate["qubits"][:-2]
            control_value = [0]
            parameter = []

        # csx gate
        if gate["name"] == "csx":
            name = "sx"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [1]
            parameter = []
        if gate["name"] == "csx_o0":
            name = "sx"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [0]
            parameter = []

        # cu gate
        if gate["name"] == "cu":
            name = "u"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [1]
            parameter = gate["params"] + [0]
        if gate["name"] == "cu_o0":
            name = "u"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [0]
            parameter = gate["params"] + [0]

        # cx gate
        if gate["name"] == "cx":
            name = "x"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [1]
            parameter = []
        if gate["name"] == "cx_o0":
            name = "x"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [0]
            parameter = []

        # cy gate
        if gate["name"] == "cy":
            name = "y"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [1]
            parameter = []
        if gate["name"] == "cy_o0":
            name = "y"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [0]
            parameter = []

        # cz gate
        if gate["name"] == "cz":
            name = "z"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [1]
            parameter = []
        if gate["name"] == "cz_o0":
            name = "z"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [0]
            parameter = []

        # h gate
        if gate["name"] == "h":
            name = gate["name"]
            target_qubit = gate["qubits"][-1:]
            control_qubit = []
            control_value = []
            parameter = []

        # id gate
        if gate["name"] == "id":
            name = "id"
            target_qubit = gate["qubits"][-1:]
            control_qubit = []
            control_value = []
            parameter = []

        # iswap gate
        if gate["name"] == "iswap":
            name = gate["name"]
            target_qubit = gate["qubits"][-2:]
            control_qubit = []
            control_value = [1]
            parameter = []

        # mcp gate
        if gate["name"] == "mcphase":
            name = "p"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [1]
            parameter = gate["params"]

        # mcx gate
        if gate["name"] == "mcx":
            name = "x"
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = [1]
            parameter = []

        # p, r, rx, ry, rz gate
        if gate["name"] in ["p", "r", "rx", "ry", "rz"]:
            name = gate["name"]
            target_qubit = gate["qubits"][-1:]
            control_qubit = []
            control_value = []
            parameter = gate["params"]

        # s, sdg gate
        if gate["name"] in ["s", "sdg"]:
            name = gate["name"]
            target_qubit = gate["qubits"][-1:]
            control_qubit = []
            control_value = []
            parameter = []

        # swap gate
        if gate["name"] == "swap":
            name = gate["name"]
            target_qubit = gate["qubits"][-2:]
            control_qubit = []
            control_value = []
            parameter = []

        # sx, sxdg, t, tdg gate
        if gate["name"] in ["sx", "sxdg", "t", "tdg"]:
            name = gate["name"]
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = []
            parameter = []

        # u gate
        if gate["name"] == "u":
            name = gate["name"]
            target_qubit = gate["qubits"][-1:]
            control_qubit = []
            control_value = []
            parameter = gate["params"] + [0]

        # x, y, z gate
        if gate["name"] in ["x", "y", "z"]:
            name = gate["name"]
            target_qubit = gate["qubits"][-1:]
            control_qubit = gate["qubits"][:-1]
            control_value = []
            parameter = []

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


def _is_instance_of_qiskit_quantumcircuit(circuit) -> bool:

    _raise_error_if_not_qiskit_installed()

    return isinstance(circuit, QuantumCircuit)
