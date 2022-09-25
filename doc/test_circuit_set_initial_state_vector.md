# quantestpy.TestCircuit.set_initial_state_vector

## TestCircuit.set_initial_state_vector(initial_state_vector)
Sets an arbitrary vector as the initial state of the circuit.

Calling this method is optional. The default is the state vector assuming all the qubits being initialized to 0.

### Parameters

#### initial_state_vector : numpy.ndarray
The state vector in the initial state.

### Examples
Use the Bell state as the initial state:
```py
>>>> tc = TestCircuit(2)
>>>> bell_state = np.array([1., 0., 0., 1.]) / np.sqrt(2.)
>>>> tc.set_initial_state_vector(bell_state)
```
