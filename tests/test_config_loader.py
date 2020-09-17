from pathlib import Path

from pytest import fixture, raises

from src.config_loader import valid_document, valid_ss_n, InvalidDocument
from src.config_loader import Worker, Company, DatesOff, HourlyConfig, load_config


def test_stupid():
    assert True


@fixture
def worker():
    return Worker(name="The Guy", dni="12345678A", ss_n=["08", "12345678", "15"])


@fixture
def company():
    return Company(
        name="The Boss", workplace="Home", cif="A12345678", ccc=["08", "12345678", "15"]
    )


@fixture
def dates_off():
    return DatesOff(weekdays=[6, 7], holidays=[11, 24])


@fixture
def hourly_config(worker, company, dates_off):
    return HourlyConfig(
        year=2020,
        month=7,
        working_hours=[9, 13, 14, 18],
        worker=worker,
        company=company,
        dates_off=dates_off,
    )


def test_valid_document():

    assert valid_document("12345678A", "dni")
    assert not valid_document("123A567A", "dni")
    assert not valid_document("123456789A", "dni")
    assert not valid_document("123456789AB", "dni")
    assert valid_document("X98765432", "cif")
    assert not valid_document("123A5678", "cif")
    assert not valid_document("X987654321", "cif")

    with raises(ValueError):
        valid_document("12345678A", "nni")


def test_valid_ss_n():

    assert valid_ss_n(["08", "1928182", "15"])
    assert valid_ss_n(["08", "01928182", "15"])
    assert not valid_ss_n(["08", "928182", "15"])
    assert not valid_ss_n(["8", "9228182", "15"])
    assert not valid_ss_n(["018", "9228182", "15"])
    assert not valid_ss_n(["18", "928182", "15", "2"])
    assert not valid_ss_n(["18", "9281832", "152"])
    assert not valid_ss_n(["18", "92818A2", "15"])
    assert not valid_ss_n(["1B", "9281832", "15"])
    assert not valid_ss_n(["15", "9281832", "Z5"])


def test_worker():

    w = Worker(name="The Guy", dni="12345678A", ss_n=["08", "12345678", "15"])
    assert w.name == "The Guy"
    assert w.dni == "12345678A"
    assert w.ss_n == ["08", "12345678", "15"]

    with raises(InvalidDocument):
        Worker(name="The Guy", dni="112345678A", ss_n=["08", "12345678", "15"])


def test_company():

    c = Company(
        name="The Boss", workplace="Home", cif="A12345678", ccc=["08", "12345678", "15"]
    )
    assert c.name == "The Boss"
    assert c.workplace == "Home"
    assert c.cif == "A12345678"
    assert c.ccc == ["08", "12345678", "15"]

    with raises(InvalidDocument):
        Company(
            name="The Boss",
            workplace="Home",
            cif="A123456778",
            ccc=["08", "12345678", "15"],
        )

    with raises(InvalidDocument):
        Company(
            name="The Boss",
            workplace="Home",
            cif="A12345678",
            ccc=["081", "12345678", "15"],
        )


def test_dates_off():

    d = DatesOff(weekdays=[6, 7], holidays=[11, 24])

    assert d.weekdays == [6, 7]
    assert d.holidays == [11, 24]

    d = DatesOff()
    assert d.weekdays == list()
    assert d.holidays == list()

    d = DatesOff(weekdays=[1, 6])
    assert d.weekdays == [1, 6]
    assert d.holidays == list()

    d = DatesOff(holidays=[6, 8, 25, 26])
    assert d.weekdays == list()
    assert d.holidays == [6, 8, 25, 26]

    with raises(ValueError):
        DatesOff(weekdays=[15])

    with raises(ValueError):
        DatesOff(holidays=[40])


def test_hourly_config(worker, company, dates_off):

    hc = HourlyConfig(
        year=2020,
        month=7,
        working_hours=[9, 13, 14, 18],
        worker=worker,
        company=company,
        dates_off=dates_off,
    )

    assert hc.year == 2020
    assert hc.month == 7
    assert hc.working_hours == [9, 13, 14, 18]
    assert hc.worker == worker
    assert hc.company == company
    assert hc.dates_off == dates_off
    assert hc.month_name == "julio"

    with raises(ValueError):
        HourlyConfig(
            year=2020,
            month=0,
            working_hours=[9, 13, 14, 18],
            worker=worker,
            company=company,
            dates_off=dates_off,
        )

    with raises(ValueError):
        HourlyConfig(
            year=2020,
            month=7,
            working_hours=[9, 14, 18],
            worker=worker,
            company=company,
            dates_off=dates_off,
        )

    with raises(ValueError):
        HourlyConfig(
            year=2020,
            month=7,
            working_hours=[9, 13, 14, 24],
            worker=worker,
            company=company,
            dates_off=dates_off,
        )


def test_read_config(hourly_config):

    assert load_config(Path("tests/example.yaml")) == hourly_config
