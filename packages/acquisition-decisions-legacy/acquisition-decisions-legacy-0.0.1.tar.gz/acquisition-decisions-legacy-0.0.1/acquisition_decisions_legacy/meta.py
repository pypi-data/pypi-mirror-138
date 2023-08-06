import re
from collections.abc import Iterator
from typing import Optional

from acquisition_sanitizer import case_sanitizer
from bs4 import BeautifulSoup, NavigableString, PageElement, ResultSet, Tag

from .dissect import capture_values


def get_category_from_title(case_title: str, find_target: str):
    regex = find_target.replace(" ", r"\s+")
    pattern = re.compile(rf"{regex}")
    cat = match.group() if (match := pattern.search(case_title)) else None

    if not cat:
        return case_title, None

    if cat not in case_title:
        return case_title, None

    case_title = case_title.replace(cat, "")
    cleaned_category = cat.replace(" ", "").title() if cat else None
    return case_title, cleaned_category


def get_title(soup: BeautifulSoup) -> tuple[Optional[str], Optional[str]]:

    category = None

    initial_location = soup.find("center", class_="caseheader")
    if not initial_location:
        return None, category

    title_location = initial_location.find("h3")
    if not title_location:
        return None, category

    text = title_location.get_text()

    target = "D E C I S I O N"
    case_title, category = get_category_from_title(text, target)
    if not category:
        target = "R E S O L U T I O N"
        case_title, category = get_category_from_title(text, target)

    case_title = case_title.title().strip().replace("\n", " ")

    return case_title, category


def get_headers(soup: BeautifulSoup) -> Optional[ResultSet]:
    """Used for picking items from the headers div

    Args:
        soup (BeautifulSoup): The source html document

    Returns:
        Optional[ResultSet]: h2 elements
    """
    center_header = soup.find("center", class_="caseheader")
    alt_header = soup.find(
        "div", class_="container case_document alternativeHeader"
    )
    if not (header_block := center_header or alt_header):
        return None
    if not (header_elements := header_block("h2")):
        return None
    return header_elements


def pick(slice: int, headers: ResultSet) -> Optional[Tag]:
    try:
        return headers[slice]
    except IndexError:
        return None
    except TypeError:
        return None


def get_citation(soup: BeautifulSoup, idx: str) -> Optional[str]:
    attrs = {"data-docid": idx}
    if not (tag := soup.find("article", attrs=attrs)):
        return None
    if not isinstance(tag.next_element, NavigableString):
        return None
    return str(tag.next_element).strip()


def get_ponente_tag(tag: Tag) -> Tag:
    while True:
        if isinstance(tag, Tag) and tag.name == "strong":
            return tag
        tag = tag.next_element


def get_ponente_text(tag: Tag) -> Optional[str]:
    if not (ponente_tag := get_ponente_tag(tag)):
        return None
    return ponente_tag.get_text().title()


def mark_start(soup: BeautifulSoup) -> tuple[BeautifulSoup, Optional[Tag]]:
    # create a new tag
    div = soup.new_tag("div")
    div["id"] = "start"

    # insert the new tag as a marker
    start_tag = soup.find("div", attrs={"align": "justify"})
    if not start_tag:
        return soup, None
    start_tag.insert_before(div)

    # return the new tag
    return soup, div


def get_ponencia(soup: BeautifulSoup):
    soup, start_tag = mark_start(soup)
    if not start_tag or not (end_tag := soup.find("hr")):
        return None

    text = str(soup)
    s = text.find(str(start_tag)) + len(str(start_tag))
    e = text.find(str(end_tag)) + len(str(end_tag))
    return text[s:e]


def get_post_ponencia(
    soup: BeautifulSoup,
    ponencia_text: str,
) -> Optional[str]:
    source = str(soup)
    terminal = source.find(ponencia_text) + len(ponencia_text)
    if not (end_tag := soup.find("doctags")):
        return None
    return source[terminal : source.find(str(end_tag))]


def get_annex(text: str) -> str:
    soup = BeautifulSoup(text, "html5lib")
    # no dividers found
    if not soup("hr"):
        return text

    # decompose first divider which marks the end of the ponencia
    soup("hr")[0].decompose()

    # revise the soup object string
    new_soup_text = str(soup)

    # no dividers found
    if not soup("hr"):
        return new_soup_text

    # use the first divider found as the terminal string
    target = soup("hr")[0]
    index = new_soup_text.find(str(target))
    new_slice = new_soup_text[:index]
    return new_slice


def cleaned_annex(
    soup: BeautifulSoup,
    ponencia_text: str,
    ponencia_footnotes: list,
) -> Optional[str]:
    # since no footnotes found in ponencia, no need to clean
    if not ponencia_footnotes:
        return None

    # get initial slice of annex after the ponencia
    raw = get_post_ponencia(soup, ponencia_text)
    if not raw:
        return None

    # get initial slice of annex after the ponencia
    return get_annex(raw)


def fn_digits(matches: ResultSet) -> Iterator:
    for match in matches:
        content = match.get_text().strip("[] ")
        if content.isdigit():
            try:
                yield int(content)
            except ValueError:
                ...


def list_note_digits(text: Optional[str]):
    """Do footnotes exist? If yes, what are the digits

    Args:
        text (Optional[str]): [description]

    Returns:
        [type]: [description]
    """
    if not text:
        return None
    soup = BeautifulSoup(text, "html5lib")
    matches = soup("sup", class_="fn")
    if not matches:
        return None
    return list(fn_digits(matches))


def get_body(soup: BeautifulSoup, idx: str) -> Optional[str]:
    matches = soup("article", attrs={"data-docid": idx})
    if not matches:
        return None
    return f"<html><body>{matches[-1]}</body></html>"


def with_unique_fn(text: str) -> Optional[str]:
    soup = BeautifulSoup(text, "html5lib")
    if not (footnotes_found := soup("sup")):
        return None
    for count, note in enumerate(footnotes_found, start=1):
        note["id"] = f"{count}"
    return str(soup)


def content_proper(text: str) -> dict:
    """Use the ruling phrase library to to be added to the calling function

    Args:
        text (str): The text of the ponencia

    Returns:
        dict: A dictionary with keys acceptable to scrapy processing pipeline.
    """
    keys = ["fallo", "voting", "ruling"]
    proper = capture_values(text)
    return {key: value for key, value in proper.items() if key in keys}


def ponencia_slice(data: dict) -> str:
    """If fallo exists in the ponencia and has already been segregated,
    remove it from the ponencia string and return the ponencia.

    Args:
        ponencia (str): [description]
        fallo (Optional[str]): [description]

    Returns:
        str: Culled ponencia
    """
    ponencia = data["ponencia"]
    fallo = data.get("fallo", None)
    return ponencia[: ponencia.find(fallo)] if fallo else ponencia


def unique_dividers(html: BeautifulSoup) -> BeautifulSoup:
    """Create unique identity of hr (line) and sup (footnote) tags

    Args:
        html (BeautifulSoup): [description]

    Returns:
        BeautifulSoup: [description]
    """

    # add unique id for each hr tag
    for count, line in enumerate(html("hr"), start=1):
        line["id"] = f"{count}"

    # add unique id for each sup tag
    for count, note in enumerate(html("sup"), start=1):
        note["id"] = f"{count}"

    return html


def get_composition(header: Tag):
    if composition_found := pick(0, header):
        if (text := composition_found.get_text()) in ["division", "en banc"]:
            return text.title()


def get_category(header: Tag):
    if category_found := pick(3, header):
        if (text := category_found.get_text()) in ["decision", "resolution"]:
            return text.title()


def initial_data(text: str, idx: str) -> dict:
    """Use the supplied parameters to generate initial data dictionary

    Args:
        text (str): The unprocessed string representing the ponencia
        idx (str): The url identifier

    Returns:
        dict: A dictionary with keys acceptable to scrapy processing pipeline.
    """
    raw_soup = BeautifulSoup(text, "html5lib")
    soup = unique_dividers(raw_soup)

    title, category_via_title = get_title(soup)
    if not title and not category_via_title:
        return {
            "case_title": None,
            "category": None,
            "composition": None,
            "category": None,
            "body": None,
            "ponencia": None,
            "annex": None,
        }

    if not (header := get_headers(soup)):
        return {
            "case_title": title,
            "category": category_via_title,
            "composition": None,
            "category": None,
            "body": None,
            "ponencia": None,
            "annex": None,
        }

    if not (ponencia := get_ponencia(soup)):
        return {
            "case_title": title,
            "category": category_via_title,
            "composition": get_composition(header),
            "category": get_category(header) or category_via_title,
            "body": None,
            "ponencia": None,
            "annex": None,
        }

    notes = list_note_digits(ponencia) if ponencia else None
    return {
        "case_title": title,
        "initial": get_citation(soup, idx),
        "composition": get_composition(header),
        "category": get_category(header) or category_via_title,
        "body": get_body(soup, idx),
        "ponencia": ponencia,
        "annex": cleaned_annex(soup, ponencia, notes) if ponencia else None,
    }


def sanitized(data: dict):
    for field in ["ponencia", "annex", "fallo", "voting", "ruling"]:
        if not data.get(field, None):
            continue
        data[field] = case_sanitizer.sanitize(data[field])
    return data
