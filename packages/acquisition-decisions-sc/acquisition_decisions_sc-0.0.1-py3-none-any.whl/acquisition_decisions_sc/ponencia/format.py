from bs4 import BeautifulSoup, NavigableString, Tag


def format(text: str):
    soup = BeautifulSoup(text, "html5lib")
    center_fixes = fix_centered_elements(soup)
    unwrap_breaks = unwrap_br_divs(center_fixes)
    return str(unwrap_breaks)


def unwrap_br_divs(soup: BeautifulSoup) -> BeautifulSoup:
    """Partial fix for 35517 and similar situations with bad divs"""
    for div in soup("div"):
        if (
            div.contents  # not empty
            and len(div.contents) == 1  # only one child
            and isinstance(div.contents[0], Tag)  # child is a tag
            and div.contents[0].name == "br"  # tag is <br>
        ):
            div.unwrap()
    return soup


def fix_centered_elements(soup: BeautifulSoup) -> BeautifulSoup:
    """
    See 42512
    """
    destroy_br_list = []
    centered_text = soup("center")

    # remove <br> tags located inside center tags
    # <center><strong><em>The Procedure in Preliminary Investigation<br/>Under Rule 112 of the 1985 Rules<br/>on Criminal Procedure</em></strong><br/></center>
    for center in centered_text:
        for child in center.descendants:
            if isinstance(child, Tag) and child.name == "br":
                destroy_br_list.append(child)
    for item in destroy_br_list:
        item.insert_before(NavigableString(" "))
        item.decompose()

    # insert <br> tags before and after the center tags
    # this should avoid the problem of bad segmentation, i.e. blockquotes look for nearest preceding paragraph / br tag
    for center in centered_text:
        center.insert_before(soup.new_tag("br"))
        center.insert_after(soup.new_tag("br"))

    return soup
