from .patterns import text_has_justice_ender


def remove_sr_jr_suffixes(raw: str) -> str:
    return raw.lower().removesuffix("sr.").removesuffix("jr.").strip(", ")


def remove_justice_enders(x: str) -> str:
    """Remove (if they exist) "J." and "C.J." ending texts which usually accompany ponente strings."""
    return x.removesuffix(m.group()) if (m := text_has_justice_ender(x)) else x


def get_surname(raw: str) -> str:
    """Remove suffiexes and J., C.J. ending texts to get the surame of the Justice."""
    raw = remove_justice_enders(raw)
    raw = remove_sr_jr_suffixes(raw)
    return raw.title()
