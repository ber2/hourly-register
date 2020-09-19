from pathlib import Path

from pytest import fixture, raises

from parser.config import is_valid_cif, is_valid_dni, is_valid_ss_n, InvalidDocument
from parser.config import Worker, Company, DatesOff, ReportData, load_config


def test_is_valid_dni():

    assert is_valid_dni("12345678A")
    assert not is_valid_dni("123A567A")
    assert not is_valid_dni("123456789A")
    assert not is_valid_dni("123456789AB")


def test_valid_document():

    assert is_valid_cif("X98765432")
    assert not is_valid_cif("123A5678")
    assert not is_valid_cif("X987654321")


def test_valid_ss_n():

    assert is_valid_ss_n(["08", "1928182", "15"])
    assert is_valid_ss_n(["08", "01928182", "15"])
    assert not is_valid_ss_n(["08", "928182", "15"])
    assert not is_valid_ss_n(["8", "9228182", "15"])
    assert not is_valid_ss_n(["018", "9228182", "15"])
    assert not is_valid_ss_n(["18", "928182", "15", "2"])
    assert not is_valid_ss_n(["18", "9281832", "152"])
    assert not is_valid_ss_n(["18", "92818A2", "15"])
    assert not is_valid_ss_n(["1B", "9281832", "15"])
    assert not is_valid_ss_n(["15", "9281832", "Z5"])


def test_worker():

    w = Worker(name="The Guy", dni="12345678A", ss_n=["08", "12345678", "15"])
    assert w.name == "The Guy"
    assert w.dni == "12345678A"
    assert w.ss_n == ["08", "12345678", "15"]
    assert w.ss_n_repr == "08 / 12345678 / 15"
    assert w.initials == "TG"

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
    assert c.ccc_repr == "08 / 12345678 / 15"

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


class TestReportData:
    def test_init(self, worker, company, dates_off):

        hc = ReportData(
            year=2020,
            month=9,
            working_hours=[9, 13, 14, 18],
            worker=worker,
            company=company,
            dates_off=dates_off,
        )

        assert hc.year == 2020
        assert hc.month == 9
        assert hc.days_in_month == 30
        assert hc.working_hours == [9, 13, 14, 18]
        assert hc.worker == worker
        assert hc.company == company
        assert hc.dates_off == dates_off
        assert hc.month_name == "Septiembre"
        assert hc.working_hours_repr == "09:00 & 13:00 & 14:00 & 18:00"
        assert hc.daily_working_hours_count == 8
        assert hc.next_month_repr == "octubre"
        assert hc.next_year == 2020

        with raises(ValueError):
            ReportData(
                year=2020,
                month=0,
                working_hours=[9, 13, 14, 18],
                worker=worker,
                company=company,
                dates_off=dates_off,
            )

        with raises(ValueError):
            ReportData(
                year=2020,
                month=7,
                working_hours=[9, 14, 18],
                worker=worker,
                company=company,
                dates_off=dates_off,
            )

        with raises(ValueError):
            ReportData(
                year=2020,
                month=7,
                working_hours=[9, 13, 14, 24],
                worker=worker,
                company=company,
                dates_off=dates_off,
            )

    def test_is_working_day(self, report_data):

        assert report_data.is_working_day(3)
        assert not report_data.is_working_day(5)
        assert not report_data.is_working_day(11)
        assert report_data.is_working_day(25)

    def test_format_line(self, report_data):

        d = 3
        expected = "3 & 09:00 & 13:00 & 14:00 & 18:00 & 8 & 0 & TG \\\\"
        assert report_data.format_line(d) == expected

        d = 5
        expected = "5 & & & & & & & \\\\"
        assert report_data.format_line(d) == expected

        d = 25
        expected = "25 & 09:00 & 13:00 & 14:00 & 18:00 & 8 & 0 & TG \\\\"
        assert report_data.format_line(d) == expected

    def test_total_working_hours(self, report_data):

        assert report_data.total_working_hours() == 160


def test_read_config(report_data):

    assert load_config(Path("tests/example.yaml")) == report_data
