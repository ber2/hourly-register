import datetime as dt


MONTH_NAMES = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}


def number_of_days_in_month(year: int, month: int) -> int:
    first_day_of_month = dt.date(year, month, 1)
    year_next = year + 1 if month == 12 else year
    month_next = month % 12 + 1
    first_day_of_next_month = dt.date(year_next, month_next, 1)

    return (first_day_of_next_month - first_day_of_month).days

