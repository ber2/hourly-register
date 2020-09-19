from parser.calendar import number_of_days_in_month, format_hour, next_month_repr, next_year


def test_number_of_days_in_month():

    assert number_of_days_in_month(2020, 2) == 29
    assert number_of_days_in_month(2021, 2) == 28
    assert number_of_days_in_month(1980, 1) == 31
    assert number_of_days_in_month(1984, 9) == 30


def test_format_hour():

    assert format_hour(3) == "03:00"
    assert format_hour(9) == "09:00"
    assert format_hour(10) == "10:00"
    assert format_hour(21) == "21:00"


def test_next_month_repr():

    assert next_month_repr(1) == "febrero"
    assert next_month_repr(7) == "agosto"
    assert next_month_repr(12) == "enero"

def test_next_year():
    assert next_year(2020, 12) == 2021

    for m in range(1, 12):
        assert next_year(2019, m) == 2019
