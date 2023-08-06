from pathlib import Path
from typing import Iterator

from dateutil.relativedelta import relativedelta as rd
from lawsql_utils.files import (
    BASE_CONTENT,
    JUSTICES_PROPER,
    load_yaml_from_path,
)
from lawsql_utils.general import parse_date_if_exists
from sqlite_utils import Database
from sqlite_utils.db import Table

DB_FILE = BASE_CONTENT.joinpath("index.db")
DB = Database(DB_FILE, use_counts_table=True)


MAX_AGE = 70
MAX_LABEL_LENGTH = 50


def justices_tbl():
    tbl = DB["Justices"]
    if tbl.exists():
        return tbl

    tbl.create(
        columns={
            "pk": int,
            "first_name": str,
            "last_name": str,
            "full_name": str,
            "suffix": str,
            "gender": str,
            "start_term": str,
            "end_term": str,
            "chief_date": str,
            "birth_date": str,
            "retire_date": str,
        },
        pk="pk",
    )

    for i in [
        "pk",
        "last_name",
        "gender",
        "start_term",
        "end_term",
        "retire_date",
    ]:
        tbl.create_index([i])

    if not tbl.has_counts_triggers:
        tbl.enable_counts()

    return load_justices(tbl)


def get_justice_records_from(p: Path) -> Iterator[dict]:
    "Remove unessential contents from .yaml file path, e.g. 'Justice' and 'Replacing'"
    for i in load_yaml_from_path(p):
        yield get_justice_from_dict(i)


def get_justice_from_dict(i: dict) -> dict:
    i.pop("Justice")
    i.pop("Replacing")
    return {
        "pk": int(i.pop("#")),
        "first_name": i.pop("First Name").strip(),
        "last_name": i.pop("Last Name").strip(),
        "suffix": s.strip() if (s := i.pop("Suffix")) else None,
        "gender": i.pop("Gender").strip(),
        "start_term": parse_date_if_exists(i.pop("Start of term")),
        "end_term": (_end := parse_date_if_exists(i.pop("End of term"))),
        "chief_date": parse_date_if_exists(i.pop("Appointed chief")),
        "birth_date": (dob := parse_date_if_exists(i.pop("Born"))),
        "retire_date": dob + rd(years=MAX_AGE) if dob else _end,
    }


def load_justices(tbl: Table):
    return tbl.insert_all(
        get_justice_records_from(JUSTICES_PROPER),
        pk="pk",
        not_null=("first_name, last_name, start_term"),
        replace=True,
    )


JUSTICES_TABLE = justices_tbl()
