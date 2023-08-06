import codecs
from pathlib import Path
from typing import Iterator, NoReturn, Optional, Union

import yaml
from yaml.parser import ParserError
from yaml.scanner import ScannerError

from .path_to_local import (
    ANNEX_HTML_FILE,
    DECISIONS_PATH,
    OLD_PATH,
    PONENCIA_HTML_FILE,
    SC_PATH,
    STATUTES_PATH,
)


def load_yaml_from_path(file_path: Path):
    "Load the contents of the .yaml file"
    with open(file_path, "r") as readfile:
        return yaml.load(readfile, Loader=yaml.FullLoader)


def load_yaml_list(file_path: Path) -> Union[NoReturn, list]:
    "Load contents of the .yaml file only if it is a valid list"
    try:
        d = load_yaml_from_path(file_path)
        if isinstance(d, list):
            return d
        raise Exception("Should be a list")
    except ScannerError as e:
        raise Exception(f"See error {e}")
    except ParserError as e:
        raise Exception(f"See error {e}")


def extract_statutes_details_only(fields: tuple = None) -> Iterator[dict]:
    "Extract relevant fields from the Statutes directory"
    if not fields:
        fields = ("numeral", "category", "law_title", "date")

    for f in STATUTES_PATH.glob("**/details.yaml"):
        data = load_yaml_from_path(f)
        yield {k: v for k, v in data.items() if k in fields}


def get_old(pk: str = "") -> Iterator[Path]:
    if pk:
        return OLD_PATH.glob(f"**/{pk}/details.yaml")
    return OLD_PATH.glob(f"**/details.yaml")


def get_sc(pk: str = "") -> Iterator[Path]:
    if pk:
        return SC_PATH.glob(f"**/{pk}/details.yaml")
    return SC_PATH.glob(f"**/details.yaml")


def get_generic() -> Iterator[Path]:
    return DECISIONS_PATH.glob("**/details.yaml")


def extract_decision_ponencia_and_annex_only(folder: Path) -> dict:
    return {"body": get_ponencia(folder), "annex": get_annex(folder)}


def get_ponencia(folder: Path) -> Optional[str]:
    return get_html(folder / PONENCIA_HTML_FILE)


def get_annex(folder: Path) -> Optional[str]:
    return get_html(folder / ANNEX_HTML_FILE)


def get_html(loc: Path) -> Optional[str]:
    return codecs.open(str(loc), "r").read() if loc.exists() else None
