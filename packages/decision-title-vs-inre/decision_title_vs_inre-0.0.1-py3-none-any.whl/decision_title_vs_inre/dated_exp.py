from typing import Optional

from bs4.element import NavigableString, Tag
from dateutil.parser import parse


def get_docketlike_text_from_em_tag_and_sibling(em_tag: Tag) -> Optional[str]:
    "Assumes `el` contains `VSINRE` pattern, e.g. <em>X v. Y</em>; the `el` + `el`'s next sibling (a string in date format) is returned if the next sibling matches a date; the combination can be used to create a citation. Consider edge cases e.g. `<em>People v. Umayam, G.R. No. 147033</em>, April 30, 2003`" ""
    try:
        if (
            isinstance(em_tag, Tag)
            and em_tag.name == "em"
            and em_tag.get_text()
            and em_tag.next_sibling
            and isinstance(em_tag.next_sibling, NavigableString)
            and parse(em_tag.next_sibling, fuzzy=True)  # is date like?
        ):
            return em_tag.get_text() + str(em_tag.next_sibling)
    except:
        ...
    return None
