import re
from typing import Optional, Pattern


def construct_indicators(*args: str) -> Pattern:
    """For each regex string passed (with `re.X`|`VERBOSE` flag enabled), create a group as a possible option; then return constructed Pattern."""
    return re.compile("|".join(rf"({i})" for i in args), re.X)


def if_match_found_return_text(p: Pattern, text: str) -> Optional[str]:
    """If pattern `p` matches anything in text, return portion of text matched"""
    return match.group(0) if (match := p.search(text)) else None


def get_first_matching_text_of_regex(regex: str, text: str) -> Optional[str]:
    """Construct pattern object from regex string with (with `re.X`|`VERBOSE` flag enabled), return portion of text matched"""
    return if_match_found_return_text(re.compile(regex, re.X), text)


def text_in_pattern_count(p: Pattern, text: str) -> int:
    """Return count of number of `pattern`s found in the text"""
    return len(list(p.finditer(text)))


def remove_pattern_if_found_else_text(p: Pattern, text: str) -> str:
    """Remove a `pattern` found in text"""
    return p.sub("", text) if p.search(text) else text


def cull_suffix(text: str) -> str:
    """Remove `the`, `of`, `,`, ` ` from the text's suffix, when existing text is passed"""
    for i in ["the", "of", ","]:
        text = text.removesuffix(i).strip()
    return text


def helper_test_match(regex: str, result: str):
    """Used for testing results of raw regexes"""
    return re.compile(regex, re.X).match(result)
