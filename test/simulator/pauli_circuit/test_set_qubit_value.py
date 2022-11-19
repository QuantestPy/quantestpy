import random
import unittest

import numpy as np

from quantestpy import PauliCircuit


class TestSetQubitValue(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.pauli_circuit.test_set_qubit_value
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.001s

    OK
    $
    """

    def test_regular(self,):
        circ = PauliCircuit(100)
        qubit_id = random.sample(range(0, 100), k=20)
        qubit_value = [random.randint(0, 1) for _ in range(20)]
        circ.set_qubit_value(qubit_id, qubit_value)

        expected_qubit_value = qubit_value
        actual_qubit_value = circ._qubit_value[qubit_id]
        self.assertTrue(np.allclose(expected_qubit_value, actual_qubit_value))
