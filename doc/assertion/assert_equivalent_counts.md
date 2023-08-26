# quantestpy.assert_equivalent_counts

## assert_equivalent_counts(counts_a, counts_b, sigma=2, msg=None)

Raises a QuantestPyAssertionError if the two sets of counts after measurement are not equal up to desired tolerance.

The test verifies that the following equation is true:
```py
abs(count_a[key] - count_b[key]) <= sigma * (sqrt(count_a[key]) + sqrt(count_b[key]))
```
for all values of `key`, where `key` is a key of the counts dictionary.

### Parameters

#### counts_a, counts_b : Dict[str, int]
The counts to compare. The keys are the bitstrings and the values are the number of times each bitstring was measured.

#### sigma : \{float, int}, optional
The number of standard deviations to use as the tolerance for the comparison.

#### msg : \{None, str}, optional
The message to be added to the error message on failure.

### Examples
```py
In [4]: counts_a
Out[4]: {'00': 100, '10': 10, '11': 3, '01': 0}

In [5]: counts_b
Out[5]: {'00': 70, '01': 0, '10': 15, '11': 4}

In [6]: qp.assert_equivalent_counts(counts_a, counts_b, sigma=1)
Traceback (most recent call last)
...
QuantestPyAssertionError: The values of key 00 are too different.
counts_a[00] = 100, counts_b[00] = 70.
Difference: 30
Tolerance: 18.
```
