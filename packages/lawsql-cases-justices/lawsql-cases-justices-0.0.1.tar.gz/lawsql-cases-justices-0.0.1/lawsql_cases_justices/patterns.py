import re
from typing import Match, Optional

END_CHIEF_STYLE = r"""
    (?P<end_chief>
        \s*
        (
            ACTING|
            Acting|
            ACTG|
            Actg\.
        )?
        \s+
        C
        \.?
        \s* # possible space
        J
        \.?
        $ # end of string
    )
"""
END_CHIEF = re.compile(END_CHIEF_STYLE, re.X)

END_JUSTICE_STYLE = r"""
    (?P<end_justice>
        \s*
        \b # possible space
        (J|M)
        \.
        $ # end of string
    )
"""
END_JUSTICE = re.compile(END_JUSTICE_STYLE, re.X)

IS_JBL_STYLE = r"""
    \b
    j
    \s*
    \.?
    \s*
    b
    \s*
    \.?
    \s*
    l
    \s*
    \.?
    \s*
"""
IS_JBL = re.compile(IS_JBL_STYLE, re.I | re.X)


def text_has_justice_ender(raw: str) -> Optional[Match]:
    return END_CHIEF.search(raw) or END_JUSTICE.search(raw)
