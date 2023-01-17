import unittest

import numpy as np

from quantestpy import QuantestPyCircuit
from quantestpy.assertion.not_entangled import assert_not_entangled
from quantestpy.exceptions import QuantestPyAssertionError


class TestAssertNotEntangled(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.assertion.not_entangled.test_assert_not_entangled
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.012s

    OK
    """

    def test_non_entanglement(self):
        qc = QuantestPyCircuit(4)
        qc.add_gate({"name": "h", "control_qubit": [], "target_qubit": [0],
                    "control_value": [], "parameter": []})
        qc.add_gate({"name": "rx", "control_qubit": [], "target_qubit": [1],
                    "control_value": [], "parameter": [np.pi/5.]})
        qc.add_gate({"name": "ry", "control_qubit": [], "target_qubit": [2],
                    "control_value": [], "parameter": [np.pi/7.]})
        qc.add_gate({"name": "rx", "control_qubit": [], "target_qubit": [0],
                    "control_value": [], "parameter": [np.pi/9.]})

        self.assertIsNone(
            assert_not_entangled(circuit=qc)
        )

    def test_entangled_bell(self):
        qc = QuantestPyCircuit(2)
        qc.add_gate({"name": "h", "control_qubit": [], "target_qubit": [0],
                    "control_value": [], "parameter": []})
        qc.add_gate({"name": "x", "control_qubit": [0], "target_qubit": [1],
                    "control_value": [1], "parameter": []})

        with self.assertRaises(QuantestPyAssertionError) as cm:
            assert_not_entangled(circuit=qc)

        expected_err_msg = "qubit 0 is entangled with qubit(s) [1].\n" \
            + "qubit 1 is entangled with qubit(s) [0]."
        self.assertEqual(cm.exception.args[0], expected_err_msg)

    def test_entangled_ghz(self):
        qc = QuantestPyCircuit(5)
        qc.add_gate({"name": "h", "control_qubit": [], "target_qubit": [0],
                    "control_value": [], "parameter": []})
        qc.add_gate({"name": "x", "control_qubit": [0], "target_qubit": [1],
                    "control_value": [1], "parameter": []})
        qc.add_gate({"name": "x", "control_qubit": [1], "target_qubit": [2],
                    "control_value": [1], "parameter": []})

        self.assertIsNone(
            assert_not_entangled(circuit=qc, qubits=[3, 4])
        )

        with self.assertRaises(QuantestPyAssertionError) as cm:
            assert_not_entangled(circuit=qc, qubits=[0])

        expected_err_msg = "qubit 0 is entangled with qubit(s) [1, 2]."
        self.assertEqual(cm.exception.args[0], expected_err_msg)
