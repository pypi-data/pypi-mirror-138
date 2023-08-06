def number_paged(regex: str) -> str:
    return rf"""
    \W*
    \b
    {regex}
    \s+
    [\d\-–\s]+ # number, dash, em-dash, space
    """


at_page_num = number_paged(r"at")
pp_num = number_paged(r"pp\.?")
note_num = number_paged(r"[Nn]ote")
