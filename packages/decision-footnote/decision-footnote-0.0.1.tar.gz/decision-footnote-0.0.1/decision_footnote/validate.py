from typing import Optional

from bs4.element import ResultSet
from lawsql_utils.html import (
    get_digit_from_fn_pattern,
    get_sup_tags,
    make_soup,
)

from .make import create_notes


def last_key_match(annex_notes: ResultSet, body_notes: ResultSet):
    return annex_notes[-1]["key"] == last_key(body_notes)


def last_key(tags: ResultSet) -> Optional[int]:
    """Get last integer of footnote, if it exists. Some cases have a '*' as ending footnote"""
    index = -1
    while True:
        try:  # traverse backwards, find first digit until end of list
            if digit := get_digit_from_fn_pattern(tags[index].get_text()):
                break
            index -= 1
        except IndexError:  # reach end of list without finding a digit
            return None  # deal 33674: all asterisks as footnotes
    return digit


def validated_footnotes(text: str, annex: str) -> Optional[list[dict]]:
    """
    Get validated list of footnotes from the annex
    1. Are there footnote numbers in the annex?
    2. Note that some cases do not contain footnotes
    3. Some improperly formatted footnotes are not yet covered
    4. Assuming footnote numbers, do they align? And have no issues?
    """
    if not (annex_notes := create_notes(annex)):
        return None

    if not (body_notes := get_sup_tags(text)):
        return None

    if not last_key_match(annex_notes, body_notes):
        return None

    if _error(annex_notes[-1]["value"]):
        annex_notes[-1]["value"] = "Error: could not format / retrieve."

    # Only return validated footnotes
    return annex_notes


def _error(text: str) -> bool:
    """
    Resolve edge case: is the last footnote value problematic?
    1. If it contains a sup tag, then yes
    2. If it contains a center tag, then possibly yes
    3. If it contains a strong tag, then possibly yes
    """
    html = make_soup(text)
    return (
        html("sup")
        or html("center")
        or html("strong")
        or "OPINION" in html.get_text()
    )
