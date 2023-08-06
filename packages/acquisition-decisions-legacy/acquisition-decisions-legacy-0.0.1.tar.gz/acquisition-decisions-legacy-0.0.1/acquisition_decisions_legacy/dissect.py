import re
from dataclasses import dataclass
from typing import Iterable, Match, Optional, Pattern

from acquisition_ruling_phrase import fetch, ordered_clause, wherefore_clause
from bs4 import BeautifulSoup, PageElement, Tag


@dataclass
class Positions:
    """
    Class for keeping track of wherefore, ordered, and voting phrases in the finale
    """

    context: str  # ideally, the finale portion (1/5th) of the raw ponencia
    index: int  # the start index of the finale portion

    @property
    def wherefore(self) -> Optional[dict]:
        """
        Return:
        1. wherefore clause as `w_clause`
        2. wherefore clause position `w_position`, factoring in offset index
        """
        if not (wf := wherefore_clause(self.context)):
            return None
        if not (phrase := self.last(wf)):  # edge cases
            return None
        return {
            "w_clause": wf,
            "w_position": self.index + phrase.start(),
        }

    @property
    def ordered_voting(self) -> Optional[dict]:
        """
        Return:
        1. ordered clause `o_clause`
        2. ordered clause start position `o_start`
        2. ordered clause position `o_position`, factoring in offset index
        3. voting clause position `v_position`, factoring in offset index
        """
        if not (ord := ordered_clause(self.context)):
            return None
        if not (phrase := self.last(ord)):  # edge cases
            return None
        return {
            "o_clause": ord,
            "o_start": phrase.start(),
            "o_position": self.index + phrase.start(),
            "v_position": self.index + phrase.end(),
        }

    def last(self, target: str) -> Optional[Match]:
        """
        1. Format the target clause properly
        2. Clause may contain characters affecting compilation of strings,
        3. e.g. parenthesis in 'WHEREFORE, judgment is hereby rendered imposing a FINE of five thousand pesos (P5,000.00)
        4. There could be several strings of target compiled pattern in the body, return last instance
        """
        # * see unresolved unescaped characters for &amp; see case 34033
        esc: str = re.escape(target)
        pattern: Pattern = re.compile(esc)
        matches: Iterable = pattern.finditer(self.context)
        items: list[Match] = list(matches)
        return items[-1] if items else None


def get_positions(text: str):
    """Finale and positions based from the finale"""
    charcount = len(text)  # character count
    get_fifth = int(charcount / 5)  # deal with modulo
    offset_index = charcount - get_fifth  # finale start
    sliced_text = text[offset_index:]
    return Positions(sliced_text, offset_index)


def try_ruling(text: str, end_index: int):
    """Is there a matching ruling phrase within text up to end_index?"""
    if (
        (phrase := fetch(text))  # phrase exists
        and (len(phrase) <= 500)  # phrase is short
        and (offset := text.find(phrase)) < end_index  # offset is sound
    ):
        return {
            "ruling": text[offset:end_index],
            "ruling_marker": phrase,
            "ruling_offset": offset,
        }
    return {}


def capture_values(text: Optional[str]) -> dict:
    """
    Accepts raw ponencia to generate potential:
    1. D: Dispositive / Fallo (wherefore clause),
    2. O: Ordered clause,
    3. R: Ruling,
    4. P: Ponencia (stripped off Fallo, Ordered clauses)

    There are four possible scenarios with respect to the text:
    1. No wherefore clause and no ordered clause
    2. No wherefore clause but with an ordered clause
    3. A wherefore clause but without an ordered clause
    4. A wherefore clause and an ordered clause

    Ideally:
    P: Text start to D's start
    R: Text start from R's offset to D's start
    D: fallo / dispositive - D's start to O's end
    V: voting block - O's end to text end
    """
    if not text:
        return {}
    positions = get_positions(text)  # wherefore (W) and ordered (O) clauses
    if not (data := positions.wherefore):
        if not (data := positions.ordered_voting):
            return {"ponencia": text, "error": "No wherefore, ordered markers"}
            # no W, no O: exit with no markers from finale slice
        o_end = data["v_position"]
        return (  # no W, with O (R maybe) from finale slice
            data
            | try_ruling(text, o_end)
            | {"voting": text[o_end:], "ponencia": text[:o_end]}
        )

    # * with W, no O (R maybe) from finale slice
    w_start = data["w_position"]  # start of wherefore clause
    data |= try_ruling(text, w_start)  # attempt a ruling
    data |= {"ponencia": text[:w_start]}  # better ponencia slice

    # * attempt O again with 'fallo cut' slice
    fallo_cut = text[w_start:]
    if not (addl := Positions(fallo_cut, w_start).ordered_voting):
        return data | split_fallo_voting(fallo_cut)  # no O from fallo cut
    else:  # * with W, and O from attempted 'fallo cut' slice
        data |= addl  # additional data sets v_position and o_start
        return data | {
            "voting": text[data["v_position"] :],
            "fallo": fallo_cut[: data["o_start"]],
        }


def split_fallo_voting(text: str):
    """
    Special hack when no ordered clause is found between Wherefore and Voting.
    1. Presumes that the text is sliced from the start of wherefore clause to end of text
    2. Get the first <em> with "J."
    3. Make a split between this combination
    4. The upper half is the fallo clause
    5. The lower half is the voting clause
    """

    def candidate_voting(e: PageElement):
        return isinstance(e, Tag) and e.name == "em" and "J." in e.get_text()

    soup = BeautifulSoup(text, "html5lib")
    if not (x := soup(candidate_voting)):
        return {"voting": None, "fallo": None}

    # get last one if more than one pattern found
    split = str(x[0])
    index = text.find(split)
    return {
        "voting": text[index:],
        "fallo": text[:index],
    }
