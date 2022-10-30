import random
import unittest

from quantestpy import FastTestCircuit
from quantestpy.exceptions import QuantestPyTestCircuitError


class TestFastTestCircuitAssertIsCorrectReg(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_fast_test_circuit_assert_is_correct_reg
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.002s

    OK
    $
    """

    def test_regular(self,):
        circ = FastTestCircuit(100)
        register = random.sample(range(0, 100), k=20)
        self.assertIsNone(
            circ._assert_is_correct_reg(reg=register, reg_name="test_register")
        )

    def test_raise_from_register_incorrect_type(self,):
        circ = FastTestCircuit(100)
        register = {0, 1, 2}
        expected_error_msg = "test_register must be a list."

        with self.assertRaises(QuantestPyTestCircuitError) as cm:
            circ._assert_is_correct_reg(reg=register, reg_name="test_register")

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_id_incorrect_type(self,):
        circ = FastTestCircuit(100)
        register = [10.]
        expected_error_msg = "Indices in test_register must be integer type."

        with self.assertRaises(QuantestPyTestCircuitError) as cm:
            circ._assert_is_correct_reg(reg=register, reg_name="test_register")

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_id_out_of_range(self,):
        circ = FastTestCircuit(100)
        register = [99, 100]
        expected_error_msg = \
            "Qubit index 100 in test_register is out of range."

        with self.assertRaises(QuantestPyTestCircuitError) as cm:
            circ._assert_is_correct_reg(reg=register, reg_name="test_register")

        self.assertEqual(cm.exception.args[0], expected_error_msg)
