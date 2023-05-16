from error_handling import ErrorChecker

# testing valid dividends values
def test_check_div_amount_valid():
    value_checker = ErrorChecker(20.1, "2020-11-23")
    assert value_checker.check_div_amount() is False

# testing invalid dividends values
def test_check_div_amount_invalid():
    value_checker = ErrorChecker("invalid_value", "2020-11-23")
    assert value_checker.check_div_amount() is True

    value_checker = ErrorChecker(0, "2020-11-23")
    assert value_checker.check_div_amount() is True

    value_checker = ErrorChecker(-3, "2020-11-23")
    assert value_checker.check_div_amount() is True

    value_checker = ErrorChecker(-0.4, "2020-11-23")
    assert value_checker.check_div_amount() is True

# testing valid transaction date values
def test_check_txn_date_valid():
    value_checker = ErrorChecker(1.23, "2020-11-23")
    assert value_checker.check_txn_date() is False

# testing invalid transaction date values
def test_check_txn_date_invalid():
    value_checker = ErrorChecker(1.23, "wrong_date")
    assert value_checker.check_txn_date() is True

    value_checker = ErrorChecker(1.23, "2001-01-01")
    assert value_checker.check_txn_date() is True
