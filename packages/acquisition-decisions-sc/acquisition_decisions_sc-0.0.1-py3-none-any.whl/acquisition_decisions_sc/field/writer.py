import re
from typing import Optional, Tuple

from lxml import etree


def get_writer(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    judge = r"(\,?\s*\bJ\b)"
    chief = r"(\,?\s*\bC\.?\s*J\b)"
    upper_curiam = r"(\bCURIAM\b)"
    title_curiam = r"(\bCuriam\b)"
    patterns = [judge, chief, upper_curiam, title_curiam]
    options = rf"({'|'.join(patterns)})"
    pattern = re.compile(options)
    return clean_writer(raw) if pattern.search(raw) else None


def clean_writer(text: str):
    text = text.removesuffix(", J,:")
    text = text.removesuffix(" J.:*")
    text = text.removesuffix("[*]")
    text = text.removesuffix(", J:")
    text = text.removesuffix(", J:")
    text = text.removesuffix(", J.:")
    text = text.removesuffix(", C.J.:")
    text = text.removesuffix(":")
    return text.title()


def spot_writer(text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    1. Get the raw writer (as formatted in html) and the cleaned writer (with extraneous details removed)
    2. The raw writer will be used for slicing
    3. The cleaned writer will be used as field data
    """
    html = etree.HTML(text)

    # spot first <strong> tags in text
    if not (spotted_list := html.xpath("//strong[1]/text()")):
        return None, None

    # is 1st item in list of strong tags = writer
    if (
        spotted_list
        and (raw := str(spotted_list[0]))
        and (cleaned := get_writer(raw))
    ):
        return raw, cleaned

    # is 2nd item in list of strong tags = writer
    elif (
        len(spotted_list) > 1
        and (raw := str(spotted_list[1]))
        and (cleaned := get_writer(raw))
    ):  #
        return raw, cleaned

    # no writer found in the first <strong> tags
    return None, None
