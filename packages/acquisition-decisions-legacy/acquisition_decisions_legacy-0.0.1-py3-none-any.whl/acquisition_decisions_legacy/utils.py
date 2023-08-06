from pathlib import Path

import httpx

from acquisition_decisions_legacy import get_legacy_sc_data

LEGACY = Path().home() / "code" / "rawlaw" / "decisions" / "legacy"


def get_html(idx: str):
    url = f"https://lawyerly.ph/juris/view/{idx}"
    filename = Path(".") / "data" / f"{url[-5:]}.html"
    if not filename.exists():
        response = httpx.get(url, verify=False)
        with open(filename, "w") as f:
            f.write(response.text)


def read_html(idx: str):
    filename = (
        Path().home()
        / "code"
        / "rawlaw"
        / "decisions"
        / "legacy"
        / f"{idx}"
        / f"body.html"
    )
    read_data = None
    with open(filename, "r") as f:
        read_data = f.read()
    return read_data


def add_ponencias():
    paths = LEGACY.glob("**/body.html")
    for path in paths:
        data = get_legacy_sc_data(path.read_text(), path.parent.stem)
        if ponencia := data.get("ponencia"):
            f = path.parent / "ponencia.html"
            if not f.exists():
                f.write_text(ponencia)
                if f.exists():
                    print(f"Added {f=}")
