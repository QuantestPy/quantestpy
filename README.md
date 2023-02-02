# QuantestPy
QuantestPy is an unit testing framework for quantum computing programs.


# Installation
We encourage installing QuantestPy via the pip tool(a python package manager).
The following command installs the core QuantestPy component.
```bash
pip install quantestpy
```


# Testing approaches with QuantestPy
You insert assert methods in your source codes.
```py
# your_source_code.py
import quantestpy as qp

state_vec = [0.7072+0j, 0, 0, 0.7072+0j]

# check that the state vector is normalized.
qp.state_vector.assert_is_normalized(state_vector_subject_to_test=state_vec)

...
```

QuantestPy provides several assert methods to check for and report failures. The following table lists the available methods:

Method | Checks that
--- | ---
[state_vector.assert_is_normalized(state_vec)](./doc/state_vector_assert_is_normalized.md) | `state_vec is normalized`
[state_vector.assert_equal(state_vec_a, state_vec_b)](./doc/state_vector_assert_equal.md) | `state_vec_a == state_vec_b`
[operator.assert_is_unitary(operator)](./doc/operator_assert_is_unitary.md) | `operator is unitary`
[operator.assert_equal(operator_a, operator_b)](./doc/operator_assert_equal.md) | `operator_a == operator_b`
[circuit.assert_equal_to_operator(circuit, operator)](./doc/circuit_assert_equal_to_operator.md) | `circuit == operator`
[circuit.assert_is_zero(circuit, qubits)](./doc/circuit_assert_is_zero.md) | `qubits in circuit are 0 states`
[circuit.assert_ancilla_is_zero(circuit, ancilla_qubits)](./doc/circuit_assert_ancilla_is_zero.md) | `ancilla_qubits in circuit are always 0 states`
[circuit.assert_equal(circuit_a, circuit_b)](./doc/circuit_assert_equal.md) | `circuit_a == circuit_b`
[assert_get_ctrl_val(circuit)](./doc/get_ctrl_val.md) | `values of control qubits for all gates`

The hyperlinks bring you to details of the methods.

# License
[Apache License 2.0](LICENSE.txt)
