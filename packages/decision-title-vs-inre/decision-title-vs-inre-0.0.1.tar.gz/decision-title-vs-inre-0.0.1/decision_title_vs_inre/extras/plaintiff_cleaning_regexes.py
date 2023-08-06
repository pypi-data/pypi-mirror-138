"""
e.g. "Court ruled in Interpacific Transit, Inc." --> signal is "in"
"""
starts_with_in_regex = r"""
    ^ # note the start
    .*
    \b
    (in|In)
    \s+
    (?= # positive lookahead for a capital letter
        [A-Z]
    )
"""

"""
e.g. "the recent case of Lozon v. NLRC" --> signal is "case of"
"""
starts_with_case_of = r"""
    .*
    \b
    case
    \s+
    of
    \s+
    (?= # positive lookahead for a capital letter
        [A-Z]
    )
"""

starts_with_eg = r"""
    ^  # note the start
    (E|e)\.
    g\.
    \,
    \s+
    (?= # positive lookahead for a capital letter
        [A-Z]
    )
"""
