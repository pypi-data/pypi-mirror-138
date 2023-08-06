import re

from bs4.element import NavigableString, Tag

from .indicators import (
    ends_in_id_ibid,
    ends_in_infra,
    ends_in_supra,
    starts_with_id_ibid,
    starts_with_infra,
    starts_with_supra,
)


def no_citation_possible(target: Tag) -> bool:
    """If either the next sibling is not a string or any testing function results in `True`, there is no citation that is possible."""
    return not next_is_str or any(
        [
            testing_function(target, regex)
            for testing_function, regex in [
                (regex_in_tag_text, ends_in_id_ibid),
                (regex_in_tag_text, ends_in_infra),
                (regex_in_tag_text, ends_in_supra),
                (regex_in_next_str, starts_with_id_ibid),
                (regex_in_next_str, starts_with_infra),
                (regex_in_next_str, starts_with_supra),
            ]
        ]
    )


def next_is_str(t: Tag) -> bool:
    """A `NavigableString` element follows `t`."""
    return (
        True
        if isinstance(t, Tag)
        and t.next_sibling
        and isinstance(t.next_sibling, NavigableString)
        else False
    )


def regex_in_tag_text(t: Tag, regex: str) -> bool:
    """
    Does the tag neighbor contain a citation?

    Examine:
    ```html
    <em>AHS/Philippines, Inc. vs. C.A., Ibid</em>., p. 329; Pizza Hut/Progressive Development Corporation vs. National Labor Relations Commission, 252 SCRA 531, 535, January 29, 1996.
    ```

    The `<em>` is the tag.

    `AHS/Philippines, Inc. vs. C.A.` is the tag case.

    The next sibling of the tag is a Navigable String.

    This next sibling contains a citation which is not the correct citation for the tag case.

    No citation exists for the tag case because of `ibid` mark (supplied by `regex` string) which is inside the tag.

    The `regex` parameter is designed to accept a pattern that ends with a latin equivalent.
    """
    return (
        True
        if isinstance(t, Tag)
        and t.name == "em"
        and (text_inside_tag := t.get_text())
        and re.compile(regex, re.X).search(text_inside_tag)
        else False
    )


def regex_in_next_str(t: Tag, regex: str) -> bool:
    """
    Does the tag neighbor contain a citation?

    Examine:
    ```html
    <em>People vs. Matrimonio,</em> supra, Fn. 33; <em>People vs. Villanueva, </em>G.R. Nos. 112164-65, February 28, 1996, 254 SCRA 202;
    ```

    The `<em>` is the tag.

    `People vs. Matrimonio` is the tag case.

    The next sibling of the tag is a Navigable String.

    This next sibling implies that since it starts with a `supra` mark (supplied by `regex` string), there is no citation for the tag case.

    The `regex` parameter is designed to accept a pattern that start with a latin equivalent.

    """

    return (
        True
        if (
            isinstance(t, Tag)
            and t.name == "em"
            and isinstance(t.next_sibling, NavigableString)
            and (next_text := str(t.next_sibling))
            and re.compile(regex, re.X).search(next_text)
        )
        else False
    )
