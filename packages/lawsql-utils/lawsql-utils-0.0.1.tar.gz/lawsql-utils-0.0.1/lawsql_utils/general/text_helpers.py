from datetime import date
from typing import Callable, Iterator, Optional

import arrow
from dateutil.parser import parse


def trim_text(raw: str, max_length: int) -> str:
    "Given a max length for a text, limit text to the same if it exceeds the length"
    return raw[:max_length] if len(raw) > max_length else raw


def format_full_date(text: str) -> date:
    "Gets a date with format February 2, 1911 and retrieves corresponding datetime object"
    return arrow.get(text, "MMMM D, YYYY").date()


def parse_date_if_exists(text: Optional[str]) -> Optional[date]:
    "If the variable contains text with more than 5 characters, parse possible date."
    if not text:
        return None
    elif text and len(text) < 5:
        return None
    elif not (parsed := parse(text)):
        return None
    return parsed.date()


def get_splits_from_slicer(raw: str, slicer: Callable) -> Iterator[str]:
    """Split `raw` text using the `slicer` until `raw` is exhausted.

    Args:
        raw (str): The string to slice
        slicer (Callable): Returns a string that has been sliced, if a match is found

    Returns:
        str: Text returned by the slicer

    Yields:
        Iterator[str]: Texts returned by the slicer or just original raw if nothing sliced.
    """
    while True:
        if sliced := slicer(raw):  # slice raw based on slicer
            yield sliced.strip()  # get successful slice
            if not (raw := raw.removeprefix(sliced).strip()):  # reduce raw
                break

        else:
            yield raw
            break
