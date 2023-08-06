import re
from typing import Optional, Tuple

from lxml import etree


def clean_category(raw: str) -> str:
    spaced = lambda z: re.compile(r"\s*".join(i for i in z), re.I | re.X)

    if spaced("decision").search(raw):
        return f"Decision"

    elif spaced("resolution").search(raw):
        return f"Resolution"

    # Some cases are improperly formatted / spelled or use different phrases
    # "Ecision", "Kapasyahan" - 29848, "Opinion" - 36567, or lack label entirely - 60046
    return f"Unknown"


def spot_category(text: str) -> Tuple[Optional[str], Optional[str]]:

    html = etree.HTML(text)

    # is last textual element in <h3> block "cleanable"?
    if (spotted_list := html.xpath("//center[1]/h3/text()[last()]")) and (
        raw := str(spotted_list[0])
    ):
        return raw, clean_category(raw)

    # is first <strong> tag in <h3> block not "Unknown"?
    elif (
        (spotted_list := html.xpath("//center[1]/h3/strong/text()"))
        and (raw := str(spotted_list[0]))
        and (cleaned := clean_category(raw)) != "Unknown"
    ):
        raw, cleaned

    return None, None
