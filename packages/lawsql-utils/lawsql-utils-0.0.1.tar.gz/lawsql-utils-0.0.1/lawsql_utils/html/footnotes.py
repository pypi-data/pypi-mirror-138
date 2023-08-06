import re
from typing import Optional

from bs4.element import ResultSet, Tag

from .formatting import make_soup


def get_sup_tags(raw: str) -> ResultSet:
    """Footnotes have the following format <sup>[1]</sup>; this gets all such formats from the raw text"""
    return make_soup(raw)("sup")


def remove_footnotes(raw: str) -> str:
    """Footnotes have the following format <sup>[1]</sup>; remove all <sup> tags from the text."""
    html = make_soup(raw)
    for tag in html("sup"):
        tag.decompose()  # remove the tag from the html object
    return html.get_text(separator=" ", strip=True)


def get_just_integers(footnote_tags: ResultSet) -> list[int]:
    """Get list of integers from list of <sup> tags"""
    return [
        int(idx)
        for footnote_tag in footnote_tags
        if (idx := footnote_tag.get_text().strip("[] ")).isdigit()
    ]


def get_digits_from_sup_tags_only(raw: str) -> list[int]:
    "Get all <sup> tags from the raw text and extract all digits from the inside of the containing brackets e.g. <sup>[1]</sup> gets 1"
    return get_just_integers(get_sup_tags(raw))


def get_asterisk_from_fn_pattern(text: str) -> Optional[str]:
    """Footnotes are exceptionally formatted in this manner: [*], [* *], etc. This function fetches the asterisks inside the [asterisk] pattern"""
    aster = re.compile(
        r"""
        \[
            (?P<aster>
                [\s\*]+
            )
        \]
        """,
        re.X,
    )
    return m.group("aster") if (m := aster.search(text)) else None


def get_digit_from_fn_pattern(text: str) -> Optional[int]:
    """Footnotes are generally formatted in this manner: [1], [2], etc. This function fetches the digit inside the [digit] pattern"""
    digit_pattern = re.compile(
        r"""
            \[
                (?P<digit_found>
                    \d+
                )
            \]
        """,
        re.X,
    )

    if not (m := digit_pattern.search(text)):
        return None

    return no if isinstance((no := int(m.group("digit_found"))), int) else None


def get_pure_digit_key_from_sup_tag(t: Tag):
    """
    In a given <sup> tag determine if it matches the criteria of <sup>[number]</sup>
    """
    if not t.get_text():
        return None  # footnotes are empty: <sup> </sup>

    if not (found := re.search(r"\d+", t.get_text())):
        return None  # when footnote string does not contain a number

    if not (found.group().isdigit()):
        return None  # what if 15A

    return found.group()
