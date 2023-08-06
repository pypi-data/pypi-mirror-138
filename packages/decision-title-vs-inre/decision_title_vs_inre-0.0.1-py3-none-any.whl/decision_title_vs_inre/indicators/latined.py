infra = r"[Ii]nfra"
supra = r"[Ss]upra"
id_ibid = r"([Ii]bid|[Ii]d\.)"  # "id" should only match id with "."; otherwise html tags with id attributes will be included.


def ends_in(regex: str) -> str:
    return rf"""
    {regex}
    \W*
    $ # end
    """


ends_in_supra = ends_in(supra)
ends_in_infra = ends_in(infra)
ends_in_id_ibid = ends_in(id_ibid)


def starts_with(regex: str) -> str:
    return rf"""
    ^ # start
    \W*
    {regex}
    """


starts_with_supra = starts_with(supra)
starts_with_infra = starts_with(infra)
starts_with_id_ibid = starts_with(id_ibid)


def is_latin(regex: str) -> str:
    return rf"""
    \W*
    (
        {regex}\W*</em>|
        \b{regex}
    )
    \.?
    \W*
    """


latin_etal = is_latin(r"et\.?\s+a[l1]")
latin_etc = is_latin(r"etc")
latin_infra = is_latin(infra)
latin_supra = is_latin(supra)
latin_id_ibid = is_latin(id_ibid)
