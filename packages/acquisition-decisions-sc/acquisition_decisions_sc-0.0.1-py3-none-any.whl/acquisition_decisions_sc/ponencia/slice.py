from typing import Optional

from bs4 import BeautifulSoup


def slice_ponencia(corpus: str, start_string: Optional[str]) -> Optional[str]:
    """
    The `writer` block or the `category` block can be the `start string`.
    Slice corpus from `start string` to the first <hr> tag.
    Being able to generate an accurate slice of the corpus ensures better segmentation, such as:
    (a) Determining the ruling portion based on the hr tag.
    (b) Itemizing the different ponencia segments.
    (c) Getting the footnotes section for each segment.

    Args:
        corpus (str): [description]
        start_string (Optional[str]): [description]

    Returns:
        Optional[str]: [description]
    """
    # check if elements existing
    if not corpus or not start_string:
        return None

    # get the start
    if not (start_mark := corpus.find(start_string)):
        return None

    # add match to length of match
    start = start_mark + len(start_string)

    # get the end, i.e. the first hr tag found
    html = BeautifulSoup(corpus, "html5lib")
    if not (find_end := html.find("hr")):
        return None

    # convert to string (note unique id from dividers)
    str_hr_tag = str(find_end)
    if not (end := corpus.index(str_hr_tag)):
        return None

    # return slice
    return corpus[start:end]
