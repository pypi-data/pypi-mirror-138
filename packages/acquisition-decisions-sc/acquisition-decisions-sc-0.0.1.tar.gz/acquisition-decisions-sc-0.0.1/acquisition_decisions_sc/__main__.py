from typing import Optional

from acquisition_case_transform import transform

from acquisition_decisions_sc.ponencia.slice import slice_ponencia

from .annex import create_dividing_attributes, get_annex
from .field import construct_body, spot_category, spot_composition, spot_writer
from .ponencia import capture_values, format, slice_ponencia


def get_modern_sc_data(raw: str, initial_text: str):
    """
    Given raw text, generate dictionary of:
    1. Ponente: name of writer of text
    2. Category: whether the text is a Decision or a Resolution
    3. Composition: whether the Court sits as a Division or En Banc
    4. Ponencia: the body of the text
    5. Annex: the portion of the text consisting of footnotes
    6. Fallo: the dispositive portion of the text
    7. Voting: participation of justices in the text
    8. Ruling: the explanation for the fallo
    9. Ruling marker: the textual start of the ruling
    10. Ruling offset: the index of the ruling marker
    """
    # sanitize content, apply formatting
    body = construct_body(raw)

    # get field to serve as start of ponencia: writer, if exists; else: category
    raw_W, ponente = spot_writer(body)
    raw_C, category = spot_category(body)
    start_slice = raw_W or raw_C

    # ponencia / annex slicing
    marked_body = create_dividing_attributes(body)

    # populate preliminary fields
    data = {
        "initial": initial_text,
        "ponente": ponente,
        "category": category,
        "composition": spot_composition(body),
        "annex": get_annex(marked_body),
    }

    # itemize fields to capture
    keys = [
        "fallo",
        "voting",
        "ruling",
        "ruling_marker",
        "ruling_offset",
        "ponencia",
        "error",
    ]

    # 'pon' includes fallo / voting; 'ponencia' culls these
    pon = pre_ponencia(marked_body, start_slice)

    # capture proper
    data.update({k: v for (k, v) in capture_values(pon).items() if k in keys})

    # modify annex, if it exists
    if annex := data.get("annex", None):
        data["annex"] = transform(annex)

    return data


def pre_ponencia(marked_body: str, start: Optional[str]):
    """
    After slicing raw ponencia, apply formatting and transformations.
    Formatting refers to cleaning the html markup, e.g. <center> tags
    Transformation refers to cleaning the content itself, e.g. improper SCRA
    """

    if not (sliced := slice_ponencia(marked_body, start)):
        return None
    return transform(format(sliced))
