import re
from typing import Optional

from bs4 import BeautifulSoup
from lxml import etree


def clean_composition(raw: str) -> str:

    soup = BeautifulSoup(raw, "html5lib")

    text = soup.get_text().title()

    if re.compile(r"banc", re.I).search(text):
        return "En Banc"

    elif re.compile(r"division", re.I).search(text):
        return "Division"

    return "Unknown"


def spot_composition(text: str) -> Optional[str]:

    html = etree.HTML(text)

    COMPOSITION_LOCATION = "//center/h2"

    spotted = html.xpath(COMPOSITION_LOCATION)[0]

    composition_raw = etree.tostring(spotted)

    if not composition_raw:
        return None

    return clean_composition(str(composition_raw))
