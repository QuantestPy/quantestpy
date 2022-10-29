import random
import unittest

import numpy as np

from quantestpy import FastTestCircuit
from quantestpy.exceptions import QuantestPyTestCircuitError


class TestFastTestCircuitSetQubitValue(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_fast_test_circuit_set_qubit_value
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.002s

    OK
    $
    """

    def test_regular(self,):
        circ = FastTestCircuit(100)
        qubit_id = random.sample(range(0, 100), k=20)
        qubit_value = [random.randint(0, 1) for _ in range(20)]
        circ.set_qubit_value(qubit_id, qubit_value)

        expected_qubit_value = qubit_value
        actual_qubit_value = circ._qubit_value[qubit_id]
        self.assertTrue(np.allclose(expected_qubit_value, actual_qubit_value))

    def test_raise_from_different_length_of_id_and_value(self,):
        circ = FastTestCircuit(100)
        qubit_id = random.sample(range(0, 100), k=20)
        qubit_value = [random.randint(0, 1) for _ in range(19)]
        expected_error_msg = \
            "Lenght of qubit_id and that of qubit_value must be same."

        with self.assertRaises(QuantestPyTestCircuitError) as cm:
            circ.set_qubit_value(qubit_id, qubit_value)

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_id_out_of_range(self,):
        circ = FastTestCircuit(100)
        qubit_id = [99, 100]
        qubit_value = [1, 1]
        expected_error_msg = "qubit_id 100 is out of range."

        with self.assertRaises(QuantestPyTestCircuitError) as cm:
            circ.set_qubit_value(qubit_id, qubit_value)

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_value_not_allowed(self,):
        circ = FastTestCircuit(100)
        qubit_id = [0, 1, 2]
        qubit_value = [1, 1, 2]
        expected_error_msg = "Elements in qubit_value must be either 0 or 1."

        with self.assertRaises(QuantestPyTestCircuitError) as cm:
            circ.set_qubit_value(qubit_id, qubit_value)

        self.assertEqual(cm.exception.args[0], expected_error_msg)
