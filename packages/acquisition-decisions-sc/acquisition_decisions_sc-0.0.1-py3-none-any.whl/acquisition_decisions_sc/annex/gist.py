from collections import deque
from typing import Deque, Optional

from bs4 import BeautifulSoup

from .extra import extraneous


def divisions(text: str):
    """Create slices using unique hr tags, previously added by divider functions"""
    html = BeautifulSoup(text, "html5lib")
    for hr in html("hr"):
        initiator = str(hr)  # unique 1
        start = text.index(initiator)
        if not (e := hr.find_next("hr")):
            continue
        terminator = str(e)  # unique 2
        end = text.index(terminator)
        yield text[start:end]


def get_annex(text: str) -> Optional[str]:
    """
    Can text be divided into parts after the ponencia? (divisions)
    Retrieve annex of the ponencia, exclude extraneous content (prune)
    Returns text consisting of <sup> tags, e.g. `<sup>[1]</sup> Lorem ipsum <sup>[2]</sup> Other footnote value;`
    """
    if not text:
        return None

    elif not (parts := divisions(text)):
        return None

    # remove empty hrs
    partitions = [part for part in parts if len(part) > 20]

    return prune(deque(partitions))


def prune(items: Deque[str]):
    """
    1. There might be extraneous blocks of text between the ponencia and the footnotes
    2. The annex might contain Notice of Judgments, an Order of Release, etc.
    3. This function prunes these extraneous blocks
    """
    while True:
        try:
            top = items[0]  # does the item exist?
        except IndexError:
            return None  # queue emptied

        if extraneous(top):
            items.popleft()  # remove item, evaluate next
        else:
            return items[0]  # non-extraneous partition is likely annex
