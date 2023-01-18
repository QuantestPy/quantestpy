import unittest

from quantestpy import QuantestPyCircuit
from quantestpy.visualization.quantestpy_circuit_drawer import \
    QuantestPyCircuitDrawer


class TestDraw(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.quantestpy_circuit.test_draw
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.001s

    OK
    $
    """

    def test_only_successful_call(self,):
        qc = QuantestPyCircuit(15)
        qc.add_gate(
            {"name": "x",
             "target_qubit": [3],
             "control_qubit": [0, 1],
             "control_value": [1, 1]}
        )
        qc.add_gate(
            {"name": "y",
             "target_qubit": [10, 11, 12],
             "control_qubit": [5],
             "control_value": [0]}
        )
        qc.add_gate(
            {"name": "swap",
             "target_qubit": [1, 7],
             "control_qubit": [0],
             "control_value": [0]}
        )
        self.assertIsInstance(qc.draw(), QuantestPyCircuitDrawer)
