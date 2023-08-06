from datetime import date
from typing import Iterator, Optional

from sqlite_utils.db import NotFoundError

from .config import JUSTICES_TABLE
from .typos import is_typo


def get_id(d: date, x: str) -> Optional[int]:
    """With a "cleaned" surname, including considered typos, get primary key (pk) of matching Justice within the date provided."""
    return pk if (pk := is_typo(x) or get_justice_id_date_name(d, x)) else None


def get_justice_id_date_name(target_date: date, surname: str) -> Optional[int]:
    """With a justice's "cleaned" surname (s) and a valid date, if only one justice row is found, return primary key (pk) of that row"""
    l = list(get_active_justices_with_date_name(target_date, surname))
    return l[0]["pk"] if l and len(l) == 1 else None


def get_justices_with_name(last_name: str) -> Iterator[dict]:
    return JUSTICES_TABLE.rows_where(
        """--sql
        lower(last_name) = lower(:last_name_param) or
        lower(replace(last_name, '-', ' ')) = lower(:last_name_param);
        """,
        {"last_name_param": last_name},
        select="pk, last_name, suffix",
    )


def get_justices_on_date(target_date: date) -> Iterator[dict]:
    return JUSTICES_TABLE.rows_where(
        """--sql
        date(start_term) < date(:target_date_param) and
        date(:target_date_param) < date(coalesce(end_term, retire_date));
        """,
        {"target_date_param": target_date},
        select="pk, last_name, suffix",
    )


def get_active_justices_with_date_name(
    target_date: date, last_name: str
) -> Iterator[dict]:
    return JUSTICES_TABLE.rows_where(
        """--sql
        (
            date(start_term) < date(:target_date_param) and
            date(:target_date_param) < date(coalesce(end_term, retire_date))
        ) and
        (
            lower(last_name) = lower(:last_name_param) or
            lower(replace(last_name, '-', ' ')) = lower(:last_name_param)
        );
        """,
        {"target_date_param": target_date, "last_name_param": last_name},
        select="pk, last_name, suffix",
    )


def get_justice_data_from_id(pk: int) -> Optional[dict]:
    """Get Justice profile row from primary key (pk), if it exists."""
    try:
        return JUSTICES_TABLE.get(pk)
    except NotFoundError:
        return None


def get_justice_surname_from_id(pk: int) -> Optional[str]:
    """Get Justice surname from primary key (pk), if it exists."""
    return row["last_name"] if (row := get_justice_data_from_id(pk)) else None


def get_justice_label_from_id(pk: int) -> Optional[str]:
    """Get Justice surname from primary key (pk), if it exists."""
    if row := get_justice_data_from_id(pk):
        if row["suffix"]:
            return f"{row['last_name']}, {row['suffix']}"
        return row["last_name"]
    return None
