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
qp.assert_normalized_state_vector(state_vector_subject_to_test=state_vec)

...
```

QuantestPy provides several assert methods to check for and report failures. The following table lists the available methods:

Method | Checks that
--- | ---
[assert_normalized_state_vector(state_vec)](./doc/assertion/assert_normalized_state_vector.md) | `state_vec is normalized`
[assert_equivalent_state_vectors(state_vec_a, state_vec_b)](./doc/assertion/assert_equivalent_state_vectors.md) | `state_vec_a == state_vec_b`
[assert_unitary_operator(operator)](./doc/assertion/assert_unitary_operator.md) | `operator is unitary`
[assert_equivalent_operators(operator_a, operator_b)](./doc/assertion/assert_equivalent_operators.md) | `operator_a == operator_b`
[assert_circuit_equivalent_to_operator(circuit, operator)](./doc/assertion/assert_circuit_equivalent_to_operator.md) | `circuit == operator`
[assert_qubit_reset_to_zero_state(circuit, qubits)](./doc/assertion/assert_qubit_reset_to_zero_state.md) | `qubits in circuit are 0 states`
[assert_ancilla_reset(circuit, ancilla_qubits)](./doc/assertion/assert_ancilla_reset.md) | `ancilla_qubits in circuit are always 0 states`
[assert_equivalent_circuits(circuit_a, circuit_b)](./doc/assertion/assert_equivalent_circuits.md) | `circuit_a == circuit_b`
[assert_unary_iteration(circuit, input_to_output)](./doc/assertion/assert_unary_iteration.md) | `circuit is the expected indexed operation`
[assert_circuit_equivalent_to_output_qubit_state(circuit, input_to_output)](./doc/assertion/assert_circuit_equivalent_to_output_qubit_state.md) | `circuit's output for the input is as expected`

The hyperlinks bring you to details of the methods.

# License
[Apache License 2.0](LICENSE.txt)
