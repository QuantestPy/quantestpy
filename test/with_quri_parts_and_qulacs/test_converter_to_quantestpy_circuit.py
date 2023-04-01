import unittest

from quri_parts.circuit import QuantumCircuit

from quantestpy import QuantestPyCircuit
from quantestpy.converter.converter_to_quantestpy_circuit import \
    cvt_input_circuit_to_quantestpy_circuit


class TestConverterToQuantestPyCircuit(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.with_quri_parts_and_qulacs.test_converter_to_quantestpy_circuit
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.101s

    OK
    """

    def test_cvt_quri_parts(self,):
        input_circuit = QuantumCircuit(3)
        qc = cvt_input_circuit_to_quantestpy_circuit(input_circuit)
        self.assertIsInstance(qc, QuantestPyCircuit)
