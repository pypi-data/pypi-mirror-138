from .__main__ import (
    VSINRE,
    VSINRE_PLUS,
    get_vs_inre_lines,
    is_single_pattern,
    nominable,
)
from .dated_exp import get_docketlike_text_from_em_tag_and_sibling
from .indicators import get_lines_from_indicators
from .inre import INRE_PATTERN, get_inre_subject_from_text
from .vs import get_parties_from_text
from .vs_em import VS_EM_PATTERN, vs_em_count, vs_em_found
