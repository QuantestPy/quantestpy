import random
import unittest

import numpy as np

from quantestpy import PauliCircuit


class TestExecuteXgate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.pauli_circuit.test_execute_x_gate
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.002s

    OK
    $
    """

    def test_qubit_value_after_x_operation_on_0(self,):
        circ = PauliCircuit(100)
        target_qubit = random.sample(range(0, 100), k=20)
        circ._execute_x_gate(target_qubit)
        qubit_value = circ._qubit_value

        self.assertTrue(np.all(qubit_value[target_qubit] == 1))
        self.assertTrue(np.all(np.delete(qubit_value, target_qubit) == 0))

    def test_qubit_value_after_x_operation_on_1(self,):
        circ = PauliCircuit(100)
        circ._qubit_value = np.array([1]*100)
        target_qubit = random.sample(range(0, 100), k=20)
        circ._execute_x_gate(target_qubit)
        qubit_value = circ._qubit_value

        self.assertTrue(np.all(qubit_value[target_qubit] == 0))
        self.assertTrue(np.all(np.delete(qubit_value, target_qubit) == 1))

    def test_qubit_phase_after_x_operation_on_0(self,):
        circ = PauliCircuit(100)
        target_qubit = random.sample(range(0, 100), k=60)
        circ._execute_x_gate(target_qubit)
        qubit_phase = circ._qubit_phase

        self.assertTrue(np.all(qubit_phase == 0.))

    def test_qubit_phase_after_x_operation_on_1(self,):
        circ = PauliCircuit(100)
        circ._qubit_value = np.array([1]*100)
        target_qubit = random.sample(range(0, 100), k=60)
        circ._execute_x_gate(target_qubit)
        qubit_phase = circ._qubit_phase

        self.assertTrue(np.all(qubit_phase == 0.))
