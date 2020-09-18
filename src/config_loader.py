from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import List, Union, Literal

import yaml

from .calendar import MONTH_NAMES


Document = Literal["dni", "cif"]


class InvalidDocument(ValueError):
    pass


def is_valid_cif(document:str) -> bool:
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

    return all([
        len(document) == 3,
        re.fullmatch(pattern_edges, document[0]),
        re.fullmatch(pattern_in, document[1]),
        re.fullmatch(pattern_edges, document[2])
    ])


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
            raise ValueError("Weekdays off not between 1 and 7: %s" % str(self.weekdays))
        if any([d not in range(1, 32) for d in self.holidays]):
            raise ValueError("Holidays given are not between 1 and 31: %s" % str(self.holidays))


@dataclass
class ReportData:
    year: 2020
    month: int
    working_hours: List[int]
    worker: Worker
    company: Company
    dates_off: DatesOff
    month_name: str = field(init=False, repr=False)

    def __post_init__(self):
        if self.month not in range(1, 13):
            raise ValueError("Invalid month: %d" % self.month)
        if len(self.working_hours) != 4 or any([h not in range(24) for h in self.working_hours]):
            raise ValueError("Invalid working hours: %s" % str(self.working_hours))
        self.month_name = MONTH_NAMES[self.month]

    def is_working_day(self, day: int) -> bool:
        return True



def load_config(filename: Path) -> ReportData:

    with open(filename, "r") as fp:
        config = yaml.safe_load(fp)

    return ReportData(config["year"],
                      config["month"],
                      config["working hours"],
                      Worker(**config["worker"]),
                      Company(**config["company"]),
                      DatesOff(**config["dates off"]))
