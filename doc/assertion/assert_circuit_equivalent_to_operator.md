# quantestpy.assert_circuit_equivalent_to_operator

## assert_circuit_equivalent_to_operator(circuit, operator_, from_right_to_left_for_qubit_ids=False, rtol=0, atol=1e-8, up_to_global_phase=False, matrix_norm_type=None, msg=None)

Raises a QuantestPyAssertionError if the circuit, which is internally converted to an operator, is not equal to the given operator up to desired tolerance.

The test verifies that the following equation is element-wise true:
```py
abs(operator_from_circuit - operator_) <= atol + rtol * abs(operator_)
```
or optionally a matrix norm of two operators satisfies
```py
matrix_norm(operator_from_circuit - operator_) <= atol + rtol * matrix_norm(operator_),
```
where `operator_from_circuit` denotes the operator converted from `circuit`.

### Parameters

#### circuit : \{quantestpy.QuantestPyCircuit, qiskit.QuantumCircuit, OpenQASM 2.0 string\}
The circuit to check. [quantestpy.QuantestPyCircuit](../simulator/quantestpy_circuit.md) is a circuit class developed in this project.

#### operator_ : \{numpy.ndarray, numpy.matrix\}
The operator desired.

#### from_right_to_left_for_qubit_ids : bool, optional
If True, when converting the circuit to an operator, the qubits of the circuit are ordered with the first qubit on the right-most side of the tensor product.

#### rtol : float, optional
Relative tolerance.

#### atol : float, optional
Absolute tolerance.

#### up_to_global_phase : bool, optional
If True, global phases are removed from both of two operators before the comparison.

#### matrix_norm_type : \{None, "operator_norm_1", "operator_norm_2", "operator_norm_inf", "Frobenius_norm", "max_norm"\}, optional
If not None, the test checks that the chosen matrix norm is within desired tolerance.

#### msg : \{None, str\}, optional
The message to be added to the error message on failure.

### Examples

```py
>>>> qc = qiskit.QuantumCircuit(3)
...: qc.h(0)  # qc.h(2) is correct.
...: qc.cx(1, 2)
...: qc.tdg(2)
...: qc.cx(0, 2)
...: qc.t(2)
...: qc.cx(1, 2)
...: qc.tdg(2)
...: qc.cx(0, 2)
...: qc.tdg(1)
...: qc.t(2)
...: qc.cx(0, 1)
...: qc.h(2)
...: qc.tdg(1)
...: qc.cx(0, 1)
...: qc.t(0)
...: qc.s(1)
>>>> op = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
...:                [0, 1, 0, 0, 0, 0, 0, 0],
...:                [0, 0, 1, 0, 0, 0, 0, 0],
...:                [0, 0, 0, 1, 0, 0, 0, 0],
...:                [0, 0, 0, 0, 1, 0, 0, 0],
...:                [0, 0, 0, 0, 0, 1, 0, 0],
...:                [0, 0, 0, 0, 0, 0, 0, 1],
...:                [0, 0, 0, 0, 0, 0, 1, 0]])  # Operator for a Toffoli circuit
>>>> qp.assert_circuit_equivalent_to_operator(qc, op)
Traceback (most recent call last):
     ...
QuantestPyAssertionError:
Not equal to tolerance rtol=0, atol=1e-08
Up to global phase: False
Mismatched elements: 32 / 64 (50%)
Max absolute difference: 1.5
Max relative difference: 1.5
 x: array([[ 0.5+0.000000e+00j,  0.5+0.000000e+00j,  0. +0.000000e+00j,
         0. +0.000000e+00j,  0.5+0.000000e+00j,  0.5+0.000000e+00j,
         0. +0.000000e+00j,  0. +0.000000e+00j],...
 y: array([[1, 0, 0, 0, 0, 0, 0, 0],
       [0, 1, 0, 0, 0, 0, 0, 0],
       [0, 0, 1, 0, 0, 0, 0, 0],...
```

Choosing the matrix norm option:
```py
>>>> qp.assert_circuit_equivalent_to_operator(qc, op, matrix_norm_type="Frobenius_norm", atol=1e-2)
Traceback (most recent call last):
     ...
QuantestPyAssertionError: matrix norm ||A-B|| 4 is larger than (atol + rtol*||B||) 0.01.
```
