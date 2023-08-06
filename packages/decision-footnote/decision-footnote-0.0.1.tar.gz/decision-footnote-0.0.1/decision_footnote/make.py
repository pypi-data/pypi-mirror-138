import re
from typing import Iterator, Optional

from bs4.element import ResultSet, Tag
from lawsql_utils.html import (
    get_asterisk_from_fn_pattern,
    get_digit_from_fn_pattern,
    make_soup,
)


def create_notes(annex: str) -> Optional[list[dict]]:
    """Split annex into list of identifiable footnotes"""
    return list(res) if (res := split_annex(*add_ids(annex))) else None


def add_ids(annex: str) -> tuple[Optional[ResultSet], str]:
    """Initialize annex for splitting into individual footnotes"""
    html = make_soup(annex)
    if notes := html("sup"):
        for i, sup in enumerate(notes, start=1):
            sup["id"] = str(i)
    return notes or None, str(html)


def split_annex(
    notes: Optional[ResultSet], source: str
) -> Optional[Iterator[dict]]:
    """Assuming pre-formatted sup tags with ids, generate dictionaries of footnotes each consisting of a key, value"""
    if not notes:
        return None
    for note in notes:
        if text := note.get_text():
            yield {
                "key": get_digit_from_fn_pattern(text)
                or get_asterisk_from_fn_pattern(text),
                "value": make_value(snippetize(note, source)),
            }


def make_value(text: str) -> str:
    """Given an HTML string with the following format <sup> </sup> X X X,  remove the sup tag; clean the string"""

    html = make_soup(text)  # recreate soup from string slice
    if html.body.sup:  # use bs4 to remove sup tag from slice
        html.body.sup.decompose()  # remove the outer html

    result = html.body.extract()  # remove empty tags from result;
    # see https://stackoverflow.com/questions/33500888/how-to-remove-tags-that-have-no-content

    [x.decompose() for x in result.find_all(lambda tag: not tag.contents)]
    # breaking this down:
    # tag: not tag.contents = tags in the soup which are empty
    # this does not yet remove <p> </p> since this contains a whitespace
    # decompose each matching tag that fits the lambda function

    # the result is now clear of empty tags
    # convert result, a soup object, back to string and remove the body tags
    # body tags occur twice in the previous result
    cleaned = re.sub(r"\<(\/)?body\>", "", str(result), 2)
    return cleaned.strip()


def snippetize(note: Tag, source: str) -> str:
    """
    Slice a snippet from a soup object until the next sup tag, i.e. content between footnote id 7 to footnote id 8
    1. Each note tag has a unique ID;
    2. Re: start index, convert tag to a string; find this unique string in the source to get the index
    3. Re: end index, find the next sup tag, if none exists, then look for the body tag
    """
    s: int = source.index(str(note))
    mark: str = str(end) if (end := note.find_next("sup")) else "</body>"
    e: int = source.index(mark)
    return source[s:e]
