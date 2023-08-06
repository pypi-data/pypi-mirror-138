import re
from typing import Union

from bs4.element import PageElement, ResultSet, Tag
from lawsql_utils.general import text_in_pattern_count
from lawsql_utils.html import extract_text_if_html

from .indicators import latin_etal
from .vs import VS_REGEX

EM_INTERNAL_VS_REGEX = rf"""
    ({latin_etal})?
    \W* # e.g. ; . ,
    {VS_REGEX}
    \W* # e.g. ; . ,
"""
EM_INTERNAL_VS = re.compile(EM_INTERNAL_VS_REGEX, re.X)

VS_EM_REGEX = rf"""
    <em>
        {EM_INTERNAL_VS_REGEX}
    </em>
    """
VS_EM_PATTERN = re.compile(VS_EM_REGEX, re.X)


def vs_em_found(tags: ResultSet[Tag]) -> bool:
    """Italics on just `vs` portion. Are all of the `vs` tags in the text the same variant? e.g. <em>vs.</em> and <em>"et. al. vs"</em> are the same variant."""
    tags_are_vs_ems = [t for t in tags if EM_INTERNAL_VS.search(t.get_text())]
    return len(tags) == len(tags_are_vs_ems)


def vs_em_count(el: Union[str, PageElement]) -> int:
    """Counts number of times "internal vs" pattern appears in text"""
    return text_in_pattern_count(EM_INTERNAL_VS, extract_text_if_html(el))
