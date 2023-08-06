from bs4.element import ResultSet, Tag
from lawsql_utils.html import identify_tags, make_soup_xaoless

from .blockquotes import assign_bq_sections, section_covered_by_paragraph
from .combiner import combine_lowercased_previous, combine_semicolon_next
from .wrapper import wrap_paragraphs_via_br_bq_indicators


def make_sections(text: str) -> ResultSet[Tag]:

    # create soup object with some defaults
    html = make_soup_xaoless(text)

    # wrap br / bq when not properly separated by <p>
    html = wrap_paragraphs_via_br_bq_indicators(html)

    # each blockquote (and its collected elements) now form a section
    html = assign_bq_sections(html)

    # prevent <p><section>; wrap
    for paragraph in html(section_covered_by_paragraph):
        paragraph.next_element.unwrap()

    # add section tag to other paragraph elements not inside blockquotes; should be <section><p>
    body = html.find("body")
    for p in body("p"):  # all <p> tags
        if p.parent == body:  # direct <p> tags in reference to body
            p.wrap(html.new_tag("section"))  # create section and wrap direct

    # combine section ending in ":" to its succeeding section
    html = combine_semicolon_next(html)

    # combine section starting with lowercase with previous section
    html = combine_lowercased_previous(html)

    # add section ids after combinations
    html = identify_tags(html, "section")

    # return ResultSet of section tags
    return html("section")
