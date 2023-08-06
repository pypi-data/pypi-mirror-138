from typing import Iterator, Optional

from bs4.element import PageElement, Tag
from lawsql_utils.general import construct_indicators

from .indicators import get_lines_from_indicators
from .inre import INRE_REGEX, inre_count
from .vs import VS_REGEX, vs_count
from .vs_em import VS_EM_REGEX, vs_em_count

VSINRE = construct_indicators(VS_REGEX, INRE_REGEX)
VSINRE_PLUS = construct_indicators(VS_REGEX, INRE_REGEX, VS_EM_REGEX)


def get_vs_inre_lines(text: str) -> Iterator[str]:
    """Will split lines from indicators found, will yield lines where any `VSINRE_PLUS` pattern is found."""
    for l in get_lines_from_indicators(text):
        if VSINRE_PLUS.search(l):
            yield l


def nominable(el: str) -> bool:
    """Does element have one `vs` string or one `in re` string"""
    return vs_count(el) == 1 or vs_em_count(el) == 1 or inre_count(el) == 1


def is_single_pattern(el: PageElement) -> bool:
    """Is there one `vs` string without red flags?; even if with red flags, is it nominable, i.e. one `vs` / `vs_em` string or one `in re` string?"""
    return (vs_count(el) == 1 and not red_flags_on_title(el)) or nominable(el)


def red_flags_on_title(tag: Tag) -> Optional[str]:
    """Text inside the tag should be: plaintiff vs. defendant"""
    text = tag.get_text()
    if len(text) < 8:
        return f"Text too short: {str(tag)}"
    elif len(text) > 150:
        return f"Text too long: {str(tag)}"
    elif text[0] == '"' or text[-1] == '"':
        return f"Text is a casename covered in quotes: {str(tag)}"
    elif text[0] == "“" or text[-1] == "”":
        return f"Text is a casename covered in quotes: {str(tag)}"
    return None
