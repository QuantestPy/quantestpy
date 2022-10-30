import random
import unittest

from quantestpy import FastTestCircuit
from quantestpy.exceptions import QuantestPyTestCircuitError


class TestFastTestCircuitAssertIsCorrectRegAndQubitVal(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.test_fast_test_circuit_assert_is_correct_reg_and_qubit_val
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    OK
    $
    """

    def test_regular(self,):
        circ = FastTestCircuit(100)
        register = random.sample(range(0, 100), k=20)
        qubit_value = [random.randint(0, 1) for _ in range(20)]
        self.assertIsNone(
            circ._assert_is_correct_reg_and_qubit_val(
                reg=register,
                reg_name="test_register",
                qubit_val=qubit_value,
                qubit_val_name="test_qubit_value"
            )
        )

    def test_raise_from_nonconsistent_length(self,):
        circ = FastTestCircuit(100)
        register = random.sample(range(0, 100), k=20)
        qubit_value = [random.randint(0, 1) for _ in range(19)]
        expected_error_msg = "Length of test_register and that of " \
            + "test_qubit_value must be the same."

        with self.assertRaises(QuantestPyTestCircuitError) as cm:
            circ._assert_is_correct_reg_and_qubit_val(
                reg=register,
                reg_name="test_register",
                qubit_val=qubit_value,
                qubit_val_name="test_qubit_value"
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)
