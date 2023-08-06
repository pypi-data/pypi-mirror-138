from typing import Iterator


def combine_regexes_as_options(regexes: list[str]) -> str:
    """Given a list of regex strings, combine them as possible options"""

    def get_regexes(regexes: list[str]) -> Iterator[str]:
        for x in regexes:
            yield x

    def set_regex(regexes: list[str]) -> str:
        return "|".join(get_regexes(regexes))

    return rf"({set_regex(regexes)})"


def construct_prefix_options(regex: str, options: list[str]) -> str:
    """
    >>> regex = r"\bCivil\s+Code"
    >>> ls = [r"[Ss]panish", r"[Oo]ld"]
    >>> x = construct_prefix_options(regex, ls)
    >>> re.compile(x).search("the Civil Code")
    None
    >>> re.compile(x).search("the spanish Civil Code")
    <re.Match object; span=(4, 22), match='spanish Civil Code'>
    """

    def set_options(regexes: list[str]) -> Iterator[str]:
        for x in regexes:
            yield rf"{x}"

    def chain_options(regexes: list[str]) -> str:
        return "|".join(set_options(regexes))

    return rf"({chain_options(options)})\s{regex}"


def construct_negative_lookbehinds(regex: str, lookbehinds: list[str]) -> str:
    """
    >>> regex = r"\bCivil\s+Code"
    >>> ls = [r"[Ss]panish", r"[Oo]ld"]
    >>> x = construct_negative_lookbehinds(regex, ls)
    >>> re.compile(x).search("the Civil Code")
    <re.Match object; span=(4, 14), match='Civil Code'>
    >>> re.compile(x).search("the Spanish Civil Code")
    None
    """

    def set_negs(regexes: list[str]) -> Iterator[str]:
        for x in regexes:
            yield rf"(?<!{x}\s)"

    def chain_negs(regexes: list[str]) -> str:
        return "".join(set_negs(regexes))

    preventers = chain_negs(lookbehinds)
    return rf"({preventers}){regex}"


def construct_acronyms(text: str, year: int = None) -> str:
    """
    >>> regex = construct_acronyms("nirc", 1939)
    >>> re.compile(regex).search("this is the 1977 N.I.R.C.")
    <re.Match object; span=(12, 25), match='1977 N.I.R.C.'>
    """
    uppered = "".join(x.upper() for x in text)
    perioded = "".join(rf"{x}\." for x in uppered)
    acronyms = rf"({uppered}\b|{perioded})"
    if year:
        acronyms = rf"{str(year)}\s+{acronyms}"
    return acronyms
