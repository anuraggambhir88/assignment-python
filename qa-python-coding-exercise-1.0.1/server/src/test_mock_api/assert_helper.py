def assert_true(value, message):
    result = value is True
    assert result, message


def assert_equal(expected, actual, type):
    result = str(expected) == str(actual)
    assert result, f'{type} actual value [{actual}] is not equal to expected value [{expected}]'