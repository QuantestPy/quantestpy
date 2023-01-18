from quantestpy.simulator.state_vector_circuit import StateVectorCircuit
from quantestpy.visualization.quantestpy_circuit_drawer import \
    QuantestPyCircuitDrawer


class StateVectorCircuitDrawer(QuantestPyCircuitDrawer):

    def __init__(self, circuit: StateVectorCircuit):
        super().__init__(circuit)


def draw_circuit(circuit: StateVectorCircuit) -> StateVectorCircuitDrawer:
    """This is the user interface."""
    svcd = StateVectorCircuitDrawer(circuit)
    svcd.draw_circuit()
    return svcd
