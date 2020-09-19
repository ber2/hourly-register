from dataclasses import dataclass, field
import datetime as dt
from pathlib import Path
import re
from typing import List, Union, Literal

import yaml

from .calendar import (
    MONTH_NAMES,
    number_of_days_in_month,
    format_hour,
    next_month_repr,
    next_year,
)


class InvalidDocument(ValueError):
    pass


def is_valid_cif(document: str) -> bool:
    doc_upper = document.upper()
    pattern = re.compile(r"[A-Z]{1}[0-9]{7,8}")
    return bool(re.fullmatch(pattern, doc_upper))


def is_valid_dni(document: str) -> bool:
    doc_upper = document.upper()
    pattern = re.compile(r"[0-9]{7,8}[A-Z]{1}")
    return bool(re.fullmatch(pattern, doc_upper))


def is_valid_ss_n(document: List[str]) -> bool:
    pattern_edges = re.compile(r"[0-9]{2}")
    pattern_in = re.compile(r"[0-9]{7,8}")

    return all(
        [
            len(document) == 3,
            re.fullmatch(pattern_edges, document[0]),
            re.fullmatch(pattern_in, document[1]),
            re.fullmatch(pattern_edges, document[2]),
        ]
    )


@dataclass
class Worker:
    name: str
    dni: str
    ss_n: List[str]
    ss_n_repr: str = field(init=False, repr=False)
    initials: str = field(init=False, repr=False)

    def __post_init__(self):
        if not is_valid_dni(self.dni):
            raise InvalidDocument("Document number %s is not a valid DNI" % self.dni)
        if not is_valid_ss_n(self.ss_n):
            raise InvalidDocument(
                "Document number %s is not a valid social security number" % self.ss_n
            )
        self.ss_n_repr = " / ".join(self.ss_n)
        self.initials = "".join([w[0].upper() for w in self.name.split(" ")])


@dataclass
class Company:
    name: str
    workplace: str
    cif: str
    ccc: List[str]
    ccc_repr: str = field(init=False, repr=False)

    def __post_init__(self):
        if not is_valid_cif(self.cif):
            raise InvalidDocument("Document number %s is not a valid DNI" % self.cif)
        if not is_valid_ss_n(self.ccc):
            raise InvalidDocument(
                "Document number %s is not a valid social security number" % self.ccc
            )
        self.ccc_repr = " / ".join(self.ccc)


@dataclass
class DatesOff:
    weekdays: List[int] = field(default_factory=list)
    holidays: List[int] = field(default_factory=list)

    def __post_init__(self):
        if any([wd not in range(1, 8) for wd in self.weekdays]):
            raise ValueError(
                "Weekdays off not between 1 and 7: %s" % str(self.weekdays)
            )
        if any([d not in range(1, 32) for d in self.holidays]):
            raise ValueError(
                "Holidays given are not between 1 and 31: %s" % str(self.holidays)
            )


@dataclass
class ReportData:
    year: 2020
    month: int
    days_in_month: int = field(init=False, repr=False)
    working_hours: List[int]
    worker: Worker
    company: Company
    dates_off: DatesOff
    month_name: str = field(init=False, repr=False)
    working_hours_repr: str = field(init=False, repr=False)
    daily_working_hours_count: int = field(init=False, repr=False)
    next_month_repr: str = field(init=False, repr=False)
    next_year: int = field(init=False, repr=False)

    def __post_init__(self):
        if self.month not in range(1, 13):
            raise ValueError("Invalid month: %d" % self.month)
        if len(self.working_hours) != 4 or any(
            [h not in range(24) for h in self.working_hours]
        ):
            raise ValueError("Invalid working hours: %s" % str(self.working_hours))
        self.month_name = MONTH_NAMES[self.month]

        self.working_hours_repr = (
            f"{format_hour(self.working_hours[0])} & "
            f"{format_hour(self.working_hours[1])} & "
            f"{format_hour(self.working_hours[2])} & "
            f"{format_hour(self.working_hours[3])}"
        )
        self.daily_working_hours_count = (
            self.working_hours[3]
            - self.working_hours[2]
            + self.working_hours[1]
            - self.working_hours[0]
        )
        self.days_in_month = number_of_days_in_month(self.year, self.month)
        self.next_month_repr = next_month_repr(self.month)
        self.next_year = next_year(self.year, self.month)

    def is_working_day(self, day: int) -> bool:
        if day in self.dates_off.holidays:
            return False

        date = dt.date(self.year, self.month, day)
        weekday = date.isocalendar()[2]

        if weekday in self.dates_off.weekdays:
            return False

        return True

    def format_line(self, day: int) -> str:
        if self.is_working_day(day):
            return (
                f"{day} & "
                f"{self.working_hours_repr} & "
                f"{self.daily_working_hours_count} & "
                f"0 & "
                f"{self.worker.initials} \\\\"
            )
        return f"{day} & & & & & & & \\\\"

    def total_working_hours(self) -> int:
        working_days = len(
            list(filter(self.is_working_day, range(1, self.days_in_month + 1)))
        )
        return self.daily_working_hours_count * working_days


def load_config(filename: Path) -> ReportData:

    with open(filename, "r") as fp:
        config = yaml.safe_load(fp)

    return ReportData(
        config["year"],
        config["month"],
        config["working hours"],
        Worker(**config["worker"]),
        Company(**config["company"]),
        DatesOff(**config["dates off"]),
    )
