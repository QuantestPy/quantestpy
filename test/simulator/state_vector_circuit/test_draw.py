import unittest

from quantestpy.simulator.state_vector_circuit import StateVectorCircuit
from quantestpy.visualization.state_vector_circuit_drawer import \
    StateVectorCircuitDrawer


class TestDraw(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.state_vector_circuit.test_draw
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.001s

    OK
    $
    """

    def test_only_successful_call(self,):
        svc = StateVectorCircuit(15)
        svc.add_gate(
            {"name": "x",
             "target_qubit": [3],
             "control_qubit": [0, 1],
             "control_value": [1, 1],
             "parameter": []}
        )
        svc.add_gate(
            {"name": "rz",
             "target_qubit": [10, 11, 12],
             "control_qubit": [5],
             "control_value": [0],
             "parameter": [0.1]}
        )
        svc.add_gate(
            {"name": "s",
             "target_qubit": [1, 7],
             "control_qubit": [0],
             "control_value": [0],
             "parameter": []}
        )
        self.assertIsInstance(svc.draw(), StateVectorCircuitDrawer)
