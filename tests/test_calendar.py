from src.calendar import number_of_days_in_month


def test_number_of_days_in_month():

    assert number_of_days_in_month(2020, 2) == 29
    assert number_of_days_in_month(2021, 2) == 28
    assert number_of_days_in_month(1980, 1) == 31
    assert number_of_days_in_month(1984, 9) == 30
