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
    12: "Diciembre",
}


def number_of_days_in_month(year: int, month: int) -> int:
    first_day_of_month = dt.date(year, month, 1)
    year_next = next_year(year, month)
    month_next = month % 12 + 1
    first_day_of_next_month = dt.date(year_next, month_next, 1)

    return (first_day_of_next_month - first_day_of_month).days


def format_hour(hour: int) -> str:
    start = f"0{hour}" if len(str(hour)) == 1 else str(hour)
    return f"{start}:00"


def next_month_repr(month: int) -> str:
    return MONTH_NAMES[month % 12 + 1].lower()


def next_year(year: int, month: int) -> int:
    return year + 1 if month == 12 else year

