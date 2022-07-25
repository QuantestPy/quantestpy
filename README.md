# QuantestPy


QuantestPy is collecting several assert methods dedicated to quantum programing. This supports two approaches for testing your codes. In one approach, you insert assert methods in your source codes:
```py
# your_source_code.py
import quantestpy

state_vec = [0.7072+0j, 0, 0, 0.7072+0j]

# check that the state vector is normalized.
quantestpy.state_vector.assert_is_normalized(
    state_vector_subject_to_test=state_vec,
    number_of_decimal_places=4
)

...
```
In the other approach, you write a test code using `QuantestPyTestCase` as a base class:
```py
# test_your_source_code.py
import quantestpy

class TestSample(quantestpy.QuantestPyTestCase):

    def test_normalization(self,):
        state_vec = [0.7072+0j, 0, 0, 0.7072+0j]

        self.state_vector_assert_is_normalized(
            state_vector_subject_to_test=state_vec,
            number_of_decimal_places=4
        )
```
which may be excecuted by typing `$ python -m unittest test_your_source_code.py`.
Note that `QuantestPyTestCase` is a subclass of `unitest.TestCase`. Therefore, you can utilize several useful methods of `unittest`.
