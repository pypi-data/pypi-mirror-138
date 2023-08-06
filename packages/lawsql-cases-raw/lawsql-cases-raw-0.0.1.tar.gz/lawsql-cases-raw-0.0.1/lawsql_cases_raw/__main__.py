from pathlib import Path
from typing import Iterator


def init_db():
    from sqlite_utils.db import Table

    from .config import DB, DECISIONS, JUSTICES, VOTING_LINES
    from .raw_sql import duplicate_elements_of_dockets, duplicate_phil_reports

    for i in [JUSTICES, DECISIONS, VOTING_LINES]:
        if not isinstance(i, Table):
            raise Exception("Missing table.")
    DB.create_view("duplicate_phils", duplicate_phil_reports, ignore=True)
    DB.create_view("duplicate_dockets", duplicate_elements_of_dockets, ignore=True)


def get_unique_decisions():
    from .config import DB, DECISIONS

    dup_phil_pks = [row["pk"] for row in DB["duplicate_phils"].rows]
    dup_docket_pks = [row["pk"] for row in DB["duplicate_dockets"].rows]
    dups = dup_phil_pks + dup_docket_pks
    for row in DECISIONS.rows:
        if row["pk"] not in dups:
            yield row


def add_old():
    from lawsql_utils.files import OLD_PATH

    from .config import DECISIONS

    DECISIONS.insert_all(get_meta(OLD_PATH), ignore=True, defaults={"per_curiam": 0})


def add_sc():
    from lawsql_utils.files import SC_PATH

    from .config import DECISIONS

    DECISIONS.insert_all(get_meta(SC_PATH), ignore=True, defaults={"per_curiam": 0})


def get_meta(folder: Path) -> Iterator[dict]:
    from lawsql_utils.files import load_yaml_from_path

    from .organizer import (
        extract_fallo,
        process_fields,
        remove_other_keys,
        updated_ponente_id,
    )

    for detail in folder.glob("**/details.yaml"):
        from casedockets.simple_matcher import updated_cat_idx

        res = remove_other_keys(load_yaml_from_path(detail))
        res |= updated_cat_idx(res) | process_fields(res, detail, folder)
        yield res | updated_ponente_id(res) | extract_fallo(detail.parent)
