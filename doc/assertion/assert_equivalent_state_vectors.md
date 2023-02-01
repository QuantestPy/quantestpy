# quantestpy.assert_equivalent_state_vectors

## assert_equivalent_state_vectors(state_vector_a, state_vector_b, rtol=0, atol=1e-8, up_to_global_phase=False, msg=None)

Raises a QuantestPyAssertionError if the two state vectors are element-wise not equal up to desired tolerance.

The test verifies that the following equation is element-wise true:
```py
abs(state_vector_a - state_vector_b) <= atol + rtol * abs(state_vector_b)
```

### Parameters

#### state_vector_a, state_vector_b : \{numpy.ndarray, list\}
The state vectors to compare.

#### rtol : float, optional
Relative tolerance.

#### atol : float, optional
Absolute tolerance.

#### up_to_global_phase : bool, optional
If True, global phases are removed from both of the two state vectors before the comparison.

#### msg : \{None, str}, optional
The message to be added to the error message on failure.


### Examples
```py
>>>> vec_a = np.array([1., 0., 1., 0.]) / np.sqrt(2.)
>>>> vec_ini = np.array([1., 0., 0., 0.])
>>>> op = np.array([[1., 0., 1j, 0.],
...:                [0., 1., 0., 1.],
...:                [1j, 0., 1., 0.],
...:                [0., -1., 0., -1j]]) / np.sqrt(2.)
>>>> vec_b = np.matmul(op, vec_ini)
>>>> qp.assert_equivalent_state_vectors(vec_a, vec_b)
Traceback (most recent call last):
     ...
QuantestPyAssertionError:
Not equal to tolerance rtol=0, atol=1e-08
Up to global phase: False
Mismatched elements: 1 / 4 (25%)
Max absolute difference: 1.
Max relative difference: 1.41421356
 x: array([0.707107, 0.      , 0.707107, 0.      ])
 y: array([0.707107+0.j      , 0.      +0.j      , 0.      +0.707107j,
       0.      +0.j      ])
```
