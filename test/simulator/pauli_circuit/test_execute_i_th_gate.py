import unittest

import numpy as np

from quantestpy import PauliCircuit


class TestExecuteIthGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.pauli_circuit.test_execute_i_th_gate
    .....
    ----------------------------------------------------------------------
    Ran 5 tests in 0.002s

    OK
    $
    """

    def setUp(self) -> None:
        self.circ = PauliCircuit(20)
        self.circ.add_gate(
            {"name": "x", "target_qubit": [0], "control_qubit": [1, 2],
             "control_value": [0, 0]})
        self.circ.add_gate(
            {"name": "y", "target_qubit": [3], "control_qubit": [4, 5],
             "control_value": [0, 0]})
        self.circ.add_gate(
            {"name": "z", "target_qubit": [6], "control_qubit": [7, 8],
             "control_value": [0, 0]})
        self.circ.add_gate(
            {"name": "swap", "target_qubit": [0, 10], "control_qubit": [],
             "control_value": []})
        self.circ.add_gate(
            {"name": "x", "target_qubit": [0], "control_qubit": [1, 2],
             "control_value": [1, 1]})

    def tearDown(self) -> None:
        del self.circ

    def test_x_gate(self,):
        self.circ._execute_i_th_gate(i=0)
        self.assertEqual(self.circ._qubit_value[0], 1)
        self.assertEqual(self.circ._qubit_phase[0], 0.)

    def test_y_gate(self,):
        self.circ._execute_i_th_gate(i=1)
        self.assertEqual(self.circ._qubit_value[3], 1)
        self.assertEqual(self.circ._qubit_phase[3], np.pi/2.)

    def test_z_gate(self,):
        self.circ._execute_i_th_gate(i=2)
        self.assertEqual(self.circ._qubit_value[6], 0)
        self.assertEqual(self.circ._qubit_phase[6], 0.)

    def test_swap_gate(self,):
        self.circ._execute_i_th_gate(i=0)
        self.circ._execute_i_th_gate(i=3)
        self.assertEqual(self.circ._qubit_value[0], 0)
        self.assertEqual(self.circ._qubit_value[10], 1)

    def test_no_gate(self,):
        self.circ._execute_i_th_gate(i=4)
        self.assertEqual(self.circ._qubit_value[0], 0)
        self.assertEqual(self.circ._qubit_phase[0], 0.)
