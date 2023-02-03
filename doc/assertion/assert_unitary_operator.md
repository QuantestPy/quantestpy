# quantestpy.assert_unitary_operator

## assert_unitary_operator(operator_subject_to_test, atol=1e-8, msg=None)

Raises a QuantestPyAssertionError if the operator is not an unitary matrix up to desired tolerance.

The test verifies that the following equation is true for all the matrix elements:
```py
abs(operator_subject_to_test * operator_subject_to_test^dagger - I) <= atol
```

### Parameters

#### operator_subject_to_test : \{numpy.ndarray, numpy.matrix\}
The operator desired to be unitary.

#### atol : float, optional
Absolute tolerance.

#### msg : \{None, str\}, optional
The message to be added to the error message on failure.


### Examples
```py
>>>> op_ini = np.array([[0., 1.], [1., 0.]])
>>>> op = np.matmul(np.array([[0., 1j], [-1j, 1.]]), op_ini)
>>>> qp.assert_unitary_operator(op)
Traceback (most recent call last):
     ...
QuantestPyAssertionError: Operator is not unitary.
m * m^+:
[[1.+0.j 0.+1.j]
 [0.-1.j 2.+0.j]]
```
