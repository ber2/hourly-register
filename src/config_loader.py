from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import List, Union, Literal

import yaml


MONTH_NAMES = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre"
}


Document = Literal["dni", "cif"]


class InvalidDocument(ValueError):
    pass


def valid_document(document: str, doctype: Document) -> bool:
    doc_upper = document.upper()

    if doctype == "dni":
        pattern = re.compile(r"[0-9]{7,8}[A-Z]{1}")
    elif doctype == "cif":
        pattern = re.compile(r"[A-Z]{1}[0-9]{7,8}")
    else:
        raise ValueError("Unknown document type: %s" % doctype)

    return bool(re.fullmatch(pattern, doc_upper))


def valid_ss_n(document: List[str]) -> bool:
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

    def __post_init__(self):
        if not valid_document(self.dni, "dni"):
            raise InvalidDocument("Document number %s is not a valid DNI" % self.dni)
        if not valid_ss_n(self.ss_n):
            raise InvalidDocument(
                "Document number %s is not a valid social security number" % self.ss_n
            )


@dataclass
class Company:
    name: str
    workplace: str
    cif: str
    ccc: List[str]

    def __post_init__(self):
        if not valid_document(self.cif, "cif"):
            raise InvalidDocument("Document number %s is not a valid DNI" % self.cif)
        if not valid_ss_n(self.ccc):
            raise InvalidDocument(
                "Document number %s is not a valid social security number" % self.ccc
            )


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
class HourlyConfig:
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



def load_config(filename: Path) -> HourlyConfig:

    with open(filename, "r") as fp:
        config = yaml.safe_load(fp)

    return HourlyConfig(config["year"],
                        config["month"],
                        config["working hours"],
                        Worker(**config["worker"]),
                        Company(**config["company"]),
                        DatesOff(**config["dates off"]))
