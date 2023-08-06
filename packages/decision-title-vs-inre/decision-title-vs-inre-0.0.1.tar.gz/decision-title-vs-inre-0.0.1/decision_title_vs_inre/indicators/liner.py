from typing import Iterator, Optional, Pattern

from lawsql_utils.general import construct_indicators, get_splits_from_slicer

from .capped import cf_cap, cite_cap, see_cap
from .latined import latin_id_ibid, latin_infra, latin_supra

regex_options_start_semicolon = [
    r"(?<!&amp);",
    latin_infra,
    latin_supra,
    latin_id_ibid,
    cf_cap,
    see_cap,
    cite_cap,
]
INDICATORS: Pattern = construct_indicators(*regex_options_start_semicolon)


def nominate_slice_from(text: str) -> Optional[str]:
    """Using `SPLITTER` pattern object which consists of various case title indicators like `see`, `supra` etc, get the first matching indicator and slice the text until such indicator is found. This will be considered a nominee as a line."""
    return text[: m.end()] if (m := INDICATORS.search(text)) else None


def get_lines_from_indicators(raw: str) -> Iterator[str]:
    """Using `get_splits_from_slicer()`, slice part of `raw` text whenever a `nominate_slice_from()` is called on the raw text; slice this nominated slice from the raw text and repeat until the raw text is exhausted."""
    for line in get_splits_from_slicer(raw, nominate_slice_from):
        yield line
