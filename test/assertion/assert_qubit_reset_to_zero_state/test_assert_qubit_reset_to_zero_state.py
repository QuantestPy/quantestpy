import unittest

from quantestpy import QuantestPyCircuit, assert_qubit_reset_to_zero_state
from quantestpy.exceptions import QuantestPyAssertionError


class TestAssertQubitResetToZeroState(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.assertion.assert_qubit_reset_to_zero_state.test_assert_qubit_reset_to_zero_state
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.008s

    OK
    """

    def test_regular_1(self,):
        qc = QuantestPyCircuit(3)
        qc.add_gate(
            {"name": "h", "target_qubit": [0], "control_qubit": [],
             "control_value": [], "parameter": []}
        )
        qc.add_gate(
            {"name": "x", "target_qubit": [2], "control_qubit": [],
             "control_value": [], "parameter": []}
        )

        self.assertIsNone(
            assert_qubit_reset_to_zero_state(
                circuit=qc,
                qubits=[1]
            )
        )

    def test_regular_2(self,):
        qc = QuantestPyCircuit(4)
        qc.add_gate(
            {"name": "h", "target_qubit": [3], "control_qubit": [],
             "control_value": [], "parameter": []}
        )
        qc.add_gate(
            {"name": "x", "target_qubit": [0], "control_qubit": [3],
             "control_value": [1], "parameter": []}
        )

        self.assertIsNone(
            assert_qubit_reset_to_zero_state(
                circuit=qc,
                qubits=[1, 2]
            )
        )

    def test_irregular_1(self,):
        qc = QuantestPyCircuit(2)
        qc.add_gate(
            {"name": "h", "target_qubit": [0], "control_qubit": [],
             "control_value": [], "parameter": []}
        )
        qc.add_gate(
            {"name": "x", "target_qubit": [1], "control_qubit": [0],
             "control_value": [1], "parameter": []}
        )

        with self.assertRaises(QuantestPyAssertionError):
            assert_qubit_reset_to_zero_state(
                circuit=qc
            )

    def test_large_a_tol_raise_no_error(self,):
        """Assertion error does not raise for Bell state when a_tol is large
        """
        qc = QuantestPyCircuit(2)
        qc.add_gate(
            {"name": "h", "target_qubit": [0], "control_qubit": [],
             "control_value": [], "parameter": []}
        )
        qc.add_gate(
            {"name": "x", "target_qubit": [1], "control_qubit": [0],
             "control_value": [1], "parameter": []}
        )

        # no error
        self.assertIsNone(
            assert_qubit_reset_to_zero_state(
                circuit=qc,
                atol=0.71
            )
        )

        # error
        with self.assertRaises(QuantestPyAssertionError):
            assert_qubit_reset_to_zero_state(
                circuit=qc,
                atol=0.7
            )
