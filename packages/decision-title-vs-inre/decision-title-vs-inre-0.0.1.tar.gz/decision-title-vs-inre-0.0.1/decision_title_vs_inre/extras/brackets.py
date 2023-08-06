def missing_brackets(text: str) -> str:
    # general cleaning
    if "(" not in text:
        text = text.rstrip(")")
    if ")" not in text:
        text = text.lstrip("(")
    if "[" not in text:
        text = text.rstrip("]")
    if "]" not in text:
        text = text.lstrip("[")
    return text
