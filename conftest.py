from pytest import fixture

from parser.config import Worker, Company, DatesOff, ReportData, load_config


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
def report_data(worker, company, dates_off):
    return ReportData(
        year=2020,
        month=9,
        working_hours=[9, 13, 14, 18],
        worker=worker,
        company=company,
        dates_off=dates_off,
    )
