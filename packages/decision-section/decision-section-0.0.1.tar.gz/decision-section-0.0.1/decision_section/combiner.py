import re
from collections import deque

from bs4 import BeautifulSoup, Tag


def combine_semicolon_next(soup: BeautifulSoup) -> BeautifulSoup:
    """If the section ends in a semicolon, combine with the next section."""

    # all sections which end in :
    sections = soup("section", text=re.compile(r":$"))

    # put in queue
    q = deque(sections)

    present = None

    # traverse queue of sections ending in ':'
    while True:

        # exhaust queue until empty
        try:
            prior = q.popleft()
        except IndexError:
            break
        if not prior:
            continue

        # subloop to get next section
        focus = prior
        while True:
            if (
                isinstance(focus.next_sibling, Tag)
                and focus.next_sibling.name == "section"
            ):
                present = focus.next_sibling
                break
            else:
                focus = focus.next_sibling
                if not focus:
                    break

        if (  # without the get_text check, <None></None> gets through
            not prior
            or not prior.get_text()
            or not present
            or not present.get_text()
        ):
            continue

        # create new tag in the same soup
        section = soup.new_tag("section")

        # merge content
        new_content = prior.contents + present.contents

        # add content to created tag
        section.extend(new_content)

        # position new tag
        prior.insert_before(section)

        # remove old tags
        prior.decompose()
        present.decompose()
    return soup


def combine_lowercased_previous(soup: BeautifulSoup) -> BeautifulSoup:
    """If the section starts with a lowercased first letter, combine with the previous section."""

    # all sections where the first character is in lowercase
    sections = [
        section
        for section in soup("section")
        if section.get_text() and section.get_text()[0].islower()
    ]

    # put in queue
    q = deque(sections)

    prior = None

    # traverse queue of sections starting with lowercase text
    while True:

        # exhaust queue until empty
        try:
            present = q.popleft()
        except IndexError:
            break
        if present is None:
            continue

        # subloop to get the immediately preceding section
        focus = present
        while True:
            if (
                isinstance(focus.previous_sibling, Tag)
                and focus.previous_sibling.name == "section"
            ):
                prior = focus.previous_sibling
                break
            else:
                focus = focus.previous_sibling
                if not focus:
                    break

        if (  # without the get_text check, <None></None> gets through
            not prior
            or not prior.get_text()
            or not present
            or not present.get_text()
        ):
            continue

        # create new tag in the same soup
        section = soup.new_tag("section")

        # merge content
        new_content = prior.contents + present.contents

        # add content to created tag
        section.extend(new_content)

        # position new tag
        prior.insert_before(section)

        # remove old tags
        prior.decompose()
        present.decompose()
    return soup
