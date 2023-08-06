from pathlib import Path

import httpx

from acquisition_decisions_sc import get_modern_sc_data

SC = Path().home() / "code" / "rawlaw" / "decisions" / "sc"


def get_html(idx: int):
    url = f"https://elibrary.judiciary.gov.ph/thebookshelf/showdocsfriendly/1/{idx}"
    filename = Path(".") / "data" / f"{url[-5:]}.html"
    if not filename.exists():
        response = httpx.get(url, verify=False)
        with open(filename, "w") as f:
            f.write(response.text)


def read_html(idx: int):
    filename = Path(".") / "data" / f"{idx}.html"
    read_data = None
    with open(filename, "r") as f:
        read_data = f.read()
    return read_data


def add_ponencias():
    paths = SC.glob("**/body.html")
    for path in paths:
        try:
            data = get_modern_sc_data(path.read_text(), path.parent.stem)
            if ponencia := data.get("ponencia"):
                f = path.parent / "ponencia.html"
                if not f.exists():
                    f.write_text(ponencia)
        except Exception as e:
            print(f"Error found: {path=}{e=}")
