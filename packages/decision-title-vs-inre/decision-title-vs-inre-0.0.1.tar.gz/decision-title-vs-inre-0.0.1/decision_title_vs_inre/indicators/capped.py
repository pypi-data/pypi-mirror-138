def pre_capital_letter(regex: str) -> str:
    return rf"""
    \b
    {regex}
    \W*
    \s+
    (?=(<em>)?[A-Z]) # exclude first capital letter;  might be italicized, e.g. "citing: <em>In re Almacen</em>"
    """


cf_cap = pre_capital_letter(
    r"""
        [Cc]
        f
        \.?
    """
)

see_cap = pre_capital_letter(
    r"""
        (
            See|
            SEE|
            see
        )
        (
            \s+
            also
        )?
    """
)

cite_cap = pre_capital_letter(
    r"""
        (
            [Qq]uot|
            [Rr]eiterat|
            [Cc]it
        )
        (
            ing|
            ed(
                \s+
                    (
                        with
                        \s+
                        approval
                        \s+
                    )?
                in
            )?
        )
    """
)
