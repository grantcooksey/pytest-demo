import pytest

# This statement is only used to make it easier to only run unit test modules.
# Integration test modules will have `pytestmark = pytest.mark.integration`
# Check out the `pytest.ini` to the list of other manually defined pytest marks
#
# Command to run unit tests: `pytest -m unit`
pytestmark = pytest.mark.unit


# pytest looks for functions prefixed with `test`
def test_basic():
    def add_2(x):
        return x + 2

    # use python standard assert to verify expectations
    assert add_2(5) == 7


# functions that aren't prefixed with test are ignored
def i_am_ignored():
    pass


# assert that an exception is raised
def test_raise_exception():
    def divide_by_zero():
        5 / 0

    with pytest.raises(ZeroDivisionError):
        divide_by_zero()


