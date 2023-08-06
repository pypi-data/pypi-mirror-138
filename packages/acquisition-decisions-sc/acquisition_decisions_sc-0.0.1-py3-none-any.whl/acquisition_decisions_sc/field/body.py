from acquisition_sanitizer import case_sanitizer
from bs4 import BeautifulSoup, Tag
from lxml import etree
from lxml.html.clean import clean_html


def construct_body(text: str):
    body_text = decode_string(text)
    cleaned_html = clean_html(body_text)
    text_with_replacements = make_replacements(cleaned_html)
    return case_sanitizer.sanitize(text_with_replacements)


def decode_string(text: str) -> str:
    BODY = "/html/body"
    html = etree.HTML(text)
    body_raw = etree.tostring(html.xpath(BODY)[0])
    text = body_raw.decode("UTF-8")
    return text


def make_replacements(text: str) -> str:
    """Pre-process text before sanitization"""
    soup = BeautifulSoup(text, "html5lib")
    soup_sans_empty_div = replace_div_empty(soup)
    soup_sans_40 = replace_div40(soup_sans_empty_div)
    sans_br_bq = br_between_bq(soup_sans_40)
    replaced_text = str(sans_br_bq)
    return replaced_text


def replace_div_empty(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Because of html-sanitizer limitation, need to replace divs which have <br> text to serve as breaklines. Per html-sanitizer:
    > "A div element is used to wrap the HTML fragment for the parser, therefore div tags are not allowed."
    See 35517
    """
    for x in soup.find_all():
        if (
            isinstance(x, Tag)
            and x.name == "div"
            and len(x.get_text(strip=True)) == 0
        ):
            br_tag = soup.new_tag("br")
            x.replace_with(br_tag)
    return soup


def replace_div40(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Because of html-sanitizer limitation, need to replace divs which mimic blockquotes. Per html-sanitizer:
    > "A div element is used to wrap the HTML fragment for the parser, therefore div tags are not allowed."
    """
    for div in soup("div", attrs={"style": "margin-left: 40px;"}):
        bq_tag = soup.new_tag("blockquote")
        bq_tag.extend(div.contents)
        div.replace_with(bq_tag)
    return soup


def br_between_bq(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Remove <br> tag in between <blockquote> tags
    Enables html-sanitizer merging of <blockquote> sibling tags
    """
    for bq in soup("blockquote"):
        if (
            isinstance(bq.next_sibling, Tag)
            and bq.next_sibling.name == "br"
            and isinstance(bq.next_sibling.next_sibling, Tag)
            and bq.next_sibling.next_sibling.name == "blockquote"
        ):
            bq.next_sibling.decompose()
    return soup
