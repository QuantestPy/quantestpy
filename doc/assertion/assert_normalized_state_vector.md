# quantestpy.assert_normalized_state_vector

## assert_normalized_state_vector(state_vector_subject_to_test, atol=1e-8, msg=None)

Raises a QuantestPyAssertionError if the state vector is not normalized up to desired tolerance.

The test verifies that `state_vector_subject_to_test` satisfies the following:
```py
abs(sqrt(|state_vector_subject_to_test|**2) - 1) <= atol
```

### Parameters

#### state_vector_subject_to_test : \{numpy.ndarray, list\}
The state vector desired to be normalized.

#### atol : float, optional
Absolute tolerance.

#### msg : \{None, str}, optional
The message to be added to the error message on failure.


### Examples
```py
>>>> vec_ini = np.array([1., 0., 0., 0.])
>>>> op = np.array([[1., 1., 0., 1j],
...:                [0., 1., 0., 1.],
...:                [1j, 0., 1., 0.],
...:                [0., -1., -1j, 0.]])
>>>> vec = np.matmul(op, vec_ini)
>>>> qp.assert_normalized_state_vector(vec)
Traceback (most recent call last):
     ...
QuantestPyAssertionError: The state vector is not normalized.
Norm: 1.4142135623730951
```
