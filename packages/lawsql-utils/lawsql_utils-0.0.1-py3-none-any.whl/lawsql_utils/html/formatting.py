import re
from typing import Pattern, Union

from bs4 import BeautifulSoup
from bs4.element import PageElement, ResultSet, Tag


def make_soup(raw: str) -> BeautifulSoup:
    return BeautifulSoup(raw, "html5lib")


def soup_xaoless(html: BeautifulSoup) -> BeautifulSoup:
    """General cleaning function"""
    for xao in html(string=re.compile(r"\xa0")):
        xao_less = str(xao).replace("\xa0", " ")  # create a new string
        xao.replace_with(xao_less)  # can't replace NavigableString x in place
    return html


def make_soup_xaoless(raw: str) -> BeautifulSoup:
    return soup_xaoless(make_soup(raw))


def make_soup_get_italicized(raw: str, p: Pattern = None) -> ResultSet[Tag]:
    "Text is converted to html, if a regex pattern `p` is supplied filter the converted html object with `<em>` tags matching `p`"
    return make_soup(raw)("em", string=p)


def identify_tags(html: BeautifulSoup, tag_name: str) -> BeautifulSoup:
    """Given a soup object and a specific tag name, return the soup object with each tag name (which contains text content) marked with an 'id'"""
    tags: ResultSet = html(tag_name)
    for idx, el in enumerate(tags, start=1):
        if el.get_text().strip():
            el["id"] = idx
        else:
            el.decompose()
    return html


def extract_text_if_html(el: Union[str, PageElement]) -> str:
    """If `el` is a `bs4` `PageElement`, get its text representation;"""
    if isinstance(el, PageElement):
        return el.get_text()
    if isinstance(el, str):
        return el
    return str(el)
