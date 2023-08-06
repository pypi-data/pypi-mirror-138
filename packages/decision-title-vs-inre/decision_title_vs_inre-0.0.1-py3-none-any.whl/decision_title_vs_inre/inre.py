import re
from typing import Optional, Union

from bs4.element import PageElement
from lawsql_utils.general import (
    remove_pattern_if_found_else_text,
    text_in_pattern_count,
)
from lawsql_utils.html import extract_text_if_html

INRE_REGEX = r"""
    (
        ^| # start
        <em>
    )
    I
    [Nn]
    \s+
    [Rr]
    [Ee]
    :? # optional
    \s+ # spaces
    (?=\w+) # one or more word characters
"""

INRE_PATTERN = re.compile(INRE_REGEX, re.X)


def inre_count(el: Union[str, PageElement]) -> int:
    return text_in_pattern_count(INRE_PATTERN, extract_text_if_html(el))


def get_inre_subject_from_text(raw: str) -> Optional[str]:
    return (
        res.strip()
        if (
            inre_count(raw) == 1
            and 3 < len(raw) < 150
            and (res := remove_pattern_if_found_else_text(INRE_PATTERN, raw))
        )
        else None
    )
