def uniform_replacements(text: str) -> str:
    if text in [
        "US",
        "U.S.",
        "US.",
        "U.S",
    ]:
        text = "United States"

    elif text in [
        "People",
        "PP",
        "Pp.",
        "eople",
    ]:
        text = "People of the Philippines"

    elif text in [
        "CA",
        "C.A.",
    ]:
        text = "Court of Appeals"

    elif text in [
        "IAC",
        "I.A.C.",
    ]:
        text = "Intermediate Appellate Court"

    elif text in [
        "CSC",
    ]:
        text = "Civil Service Commission"

    elif text in [
        "ECC",
        "Employees’ Compensation Commission",
        "Employees' Compensation Commission",
    ]:
        text = "Employees Compensation Commission"

    elif text in [
        "GSIS",
        "Gsis",
    ]:
        text = "Government Service Insurance System"

    elif text in [
        "NLRC",
        "Nlrc",
        "Labor Relations Commission",
    ]:
        text = "National Labor Relations Commission"

    elif text in [
        "PNB",
        "Pnb",
    ]:
        text = "Philippine National Bank"

    elif text in [
        "BPI",
        "Bank of the Phil. Islands",
    ]:
        text = "Bank of the Phil. Islands"

    elif text in ["COMELEC", "Comelec"]:
        text = "Commission on Elections"

    elif text in ["COA"]:
        text = "Commission on Audit"

    elif text in ["SEC"]:
        text = "Securities and Exchange Commission"

    elif text in ["CIR", "C.I.R."]:
        text = "Commissioner of Internal Revenue"

    elif text in [
        "The Government of the Philippine Islands",
        "Government of the Philippine Islands",
        "Government of the Philippines Islands",
        "Government of Philippine Islands",
        "Government of the Philippines",
        "Government of the P.I.",
        "Government of P.I",
    ]:
        text = "Government"

    elif text in [
        "Republic of the Phil.",
        "Republic of the Philippines",
    ]:
        text = "Republic"

    return text
