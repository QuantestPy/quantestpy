# quantestpy.assert_equivalent_operators

## assert_equivalent_operators(operator_a, operator_b, rtol=0, atol=1e-8, up_to_global_phase=False, matrix_norm_type=None, msg=None)

Raises a QuantestPyAssertionError if the two operators are not equal up to desired tolerance.

The test verifies that the following equation is element-wise true:
```py
abs(operator_a - operator_b) <= atol + rtol * abs(operator_b)
```
or optionally a matrix norm of the two operators satisfies
```py
matrix_norm(operator_a - operator_b) <= atol + rtol * matrix_norm(operator_b)
```

### Parameters

#### operator_a, operator_b : \{numpy.ndarray, numpy.matrix\}
The operators to compare.

#### rtol : float, optional
Relative tolerance.

#### atol : float, optional
Absolute tolerance.

#### up_to_global_phase : bool, optional
If True, global phases are removed from both of the two operators before the comparison.

#### matrix_norm_type : \{None, "operator_norm_1", "operator_norm_2", "operator_norm_inf", "Frobenius_norm", "max_norm"\}, optional
If not None, the test checks that the chosen matrix norm is within desired tolerance.

#### msg : \{None, str\}, optional
The message to be added to the error message on failure.


### Examples
```py
>>>> op_a = np.array([[1., 0., 1j, 0.],
...:                  [0., 1., 0., 1.],
...:                  [1j, 0., 1., 0.],
...:                  [0., -1., 0., -1j]]) / np.sqrt(2.)
>>>> op_b = np.array([[1., 0., 1j, 0.],
...:                  [0., 1., 0., 1.],
...:                  [1j, 0., 1., 0.],
...:                  [0., 1., 0., 1j]]) / np.sqrt(2.)
>>>> qp.assert_equivalent_operators(op_a, op_b)
Traceback (most recent call last):
     ...
QuantestPyAssertionError:
Not equal to tolerance rtol=0, atol=1e-08
Up to global phase: False
Mismatched elements: 2 / 16 (12.5%)
Max absolute difference: 1.41421356
Max relative difference: 2.
 x: array([[ 0.707107+0.j      ,  0.      +0.j      ,  0.      +0.707107j,
         0.      +0.j      ],
       [ 0.      +0.j      ,  0.707107+0.j      ,  0.      +0.j      ,...
 y: array([[0.707107+0.j      , 0.      +0.j      , 0.      +0.707107j,
        0.      +0.j      ],
       [0.      +0.j      , 0.707107+0.j      , 0.      +0.j      ,...
```

Choosing the matrix norm option:
```py
>>>> qp.assert_equivalent_operators(op_a, op_b, matrix_norm_type="operator_norm_2", atol=1e-4)
Traceback (most recent call last):
     ...
QuantestPyAssertionError: matrix norm ||A-B|| 2 is larger than (atol + rtol*||B||) 0.0001.
```
