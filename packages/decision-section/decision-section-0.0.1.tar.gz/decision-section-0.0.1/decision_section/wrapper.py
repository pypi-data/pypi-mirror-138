from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from lawsql_utils.html import containerize_next, identify_tags


def fix_first_element(html: BeautifulSoup) -> BeautifulSoup:
    """First element of body has no tag, wrap on next <br> or <p>"""
    elem = html.body.next_element
    if isinstance(elem, NavigableString):
        html = containerize_next(elem, html)
    return html


def wrap_breaklines(html) -> BeautifulSoup:
    """
    Adds a wrapping container element `<p>` to the next sibling of `<br>` elements when this next sibling is an appropriate string or tag. see 66230, 35145
    """
    breaklines = html("br")
    for breakline in breaklines:
        try:
            item = breakline.next_sibling

            if isinstance(item, NavigableString):
                html = containerize_next(item, html)

            elif isinstance(item, Tag) and item.name in [
                "strong",
                "em",
                "center",  # see 35049 (center after br)
            ]:
                html = containerize_next(item, html)

        except AttributeError:  # in case no next_sibling attribute
            continue
    return html


def wrap_blockquotes(html) -> BeautifulSoup:
    """
    Adds a wrapping container element `<p>` to the next sibling of `<blockquote>` elements when this next sibling is an appropriate string. see 35140
    """
    blockquotes = html("blockquote")
    for blockquote in blockquotes:
        try:
            item = blockquote.next_sibling
            if isinstance(item, NavigableString):
                html = containerize_next(item, html)
        except AttributeError:  # in case no next_sibling attribute
            continue
    return html


def wrap_paragraphs_via_br_bq_indicators(html: BeautifulSoup) -> BeautifulSoup:
    """Because of improper formatting, wrap certain elements in `<p>` tags so that these can be properly counted.

    Args:
        html (BeautifulSoup): [description]

    Returns:
        BeautifulSoup: [description]
    """
    html = fix_first_element(html)
    html = wrap_breaklines(html)
    html = wrap_blockquotes(html)
    html = identify_tags(html, "p")
    html = identify_tags(html, "blockquote")
    return html
