import re
from typing import NamedTuple, Optional, Union

from bs4.element import PageElement
from lawsql_utils.general import text_in_pattern_count
from lawsql_utils.html import extract_text_if_html


def vs_count(el: Union[str, PageElement]) -> int:
    return text_in_pattern_count(VS_PATTERN, extract_text_if_html(el))


VS_RAW_REGEX = r"""
    (
        v\.\s*s\s*\.
        |
        vs\.?
        |
        v\.
    )
"""

VS_REGEX = rf"\s*\b{VS_RAW_REGEX}\s*"

VS_PATTERN = re.compile(VS_REGEX, re.X)


class Parties(NamedTuple):
    plaintiff: str
    defendant: str


def get_parties_from_text(text: str) -> Optional[Parties]:
    return (
        Parties(vs_list[0].strip(), vs_list[2].strip())
        if (
            vs_count(text) == 1
            and (vs_list := VS_PATTERN.split(text))
            and len(vs_list) == 3  # second element is vs
            and len(vs_list[0]) < 120
            and len(vs_list[2]) < 120
        )
        else None
    )
