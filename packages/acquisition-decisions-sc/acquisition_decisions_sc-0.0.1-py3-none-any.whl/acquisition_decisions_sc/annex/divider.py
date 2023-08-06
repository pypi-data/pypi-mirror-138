from bs4 import BeautifulSoup, Tag


def unique_dividers(html: BeautifulSoup) -> BeautifulSoup:
    """Create unique identity of hr (line) and sup (footnote) tags"""

    # add unique id for each hr tag
    for count, line in enumerate(html("hr"), start=1):
        line["id"] = f"{count}"

    # add unique id for each sup tag
    for count, note in enumerate(html("sup"), start=1):
        note["id"] = f"{count}"

    return html


def check_first_footnote_in_divider(html: BeautifulSoup) -> BeautifulSoup:
    """
    See problem situation:

    ```html
    <sup style="color: rgb(255, 0, 0);">
    <hr align="LEFT" noshade="noshade" size="1" width="60%">[1]
    </sup>
    ```

    Issues:
    1. The sup tag contains the hr tag
    2. The annex begins with <hr>
    3. The opening <sup> tag is before the <hr>
    4. The resulting annex: <sup>[1]</sup> is not included

    Occurences:
    1. 33979
    2. 33430
    3. 34376
    """
    if not html("hr"):
        return html
    if not isinstance((footnote_tag := html("hr")[0].parent), Tag):
        return html
    if not footnote_tag.name == "sup":
        return html

    # add an initial hr tag
    new_hr = html.new_tag("hr", id="1")

    # add prior to footnote
    footnote_tag.insert_before(new_hr)

    # look for erroneous hr tag
    old_hr = next(c for c in footnote_tag.children if c.name == "hr")

    # remove erroneous hr tag
    old_hr.decompose()

    return html


def force_divide(html: BeautifulSoup) -> BeautifulSoup:
    """
    Deals with edge case 34346: no HR tag between the body and the annex;
    Deals with edge case 35293: footnotes exist but no annex
    """
    # get all footnotes with text consisting of [*] or [1]
    alpha_footnotes = html("sup", text="*") or html("sup", text="[1]")

    if not alpha_footnotes or len(alpha_footnotes) == 1:
        return html

    # add an initial hr tag
    new_hr = html.new_tag("hr", id="100")

    # add prior to footnote for PostCorpus
    alpha_footnotes[1].insert_before(new_hr)

    return html


def create_dividing_attributes(text: str) -> str:
    """Corpus is marked with unique dividers"""
    soup = BeautifulSoup(text, "html5lib")

    # mark footnotes and dividers
    marked = unique_dividers(soup)

    # deal with problematic first footnote
    problem_note = check_first_footnote_in_divider(marked)

    # deal with no divider between ponencia and annex
    edge = force_divide(problem_note)

    # convert back to str
    content = str(edge)

    # return raw html markup as a string
    return content
