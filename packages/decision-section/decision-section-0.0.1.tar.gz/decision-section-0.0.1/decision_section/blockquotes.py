from collections import deque

from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString, ResultSet
from lawsql_utils.html import wrap_in_tag


def blockquote_parent(t: BeautifulSoup):
    """
    Utilized as soup filter;
    Return blockquote whose parent tag is not a blockquote
    This prevents the calling of two blocksquotes such as in the following example
    <blockquote id="2"> <p id="8"><body>Section 16. Classification. - For the purpose of classification, the contracting business includes any or all of the following branches.</body></p> <blockquote id="3">   (a) General engineering contracting;    (b)  General building contracting; and   (c)  Specialty contracting.    </blockquote> </blockquote>
    In the example above, only the parent blockquote would be returned
    """
    return (
        isinstance(t, Tag)
        and t.name == "blockquote"
        and isinstance(t.parent, Tag)
        and t.parent.name != "blockquote"
    )


def section_covered_by_paragraph(t: BeautifulSoup):
    """
    Utilized as soup filter;
    Return paragraph whose immediate next element child is a section.
    """
    return (
        isinstance(t, Tag)
        and t.name == "p"
        and isinstance(t.next_element, Tag)
        and t.next_element.name == "section"
    )


def make_partitions(blockquotes: ResultSet[Tag]):
    """
    1. The association of bs4 elements is done backwards.
    2. Starting from the blockquote element, proceed to the previous sibling until it reaches a paragraph indicator such as a <p>
    3. For every element that is not an indicator, add to an items queue
    4. Upon breaking from the backwards searching process, append items queue to the collections queue
    5. Note that there are two queues involved in the process
    6. First is queue of collections with the blockquote as the base of each collection
    7. Each collection, in turn, consists of a queue of bs4 elements associated to such blockquote.
    """

    collections: BeautifulSoup = deque([])
    for blockquote in blockquotes:
        # add the blockquote element to the items queue
        items = deque([blockquote])
        prev = blockquote.previous_sibling
        while True:
            if isinstance(prev, Tag) and prev.name != "p":
                items.appendleft(prev)  # not paragraph element

            elif (
                isinstance(prev, Tag)
                and prev.name == "p"
                and prev.get("align")
                and prev.get("align") == "center"
            ):  # prev is a paragraph but is centered, see 66190
                items.appendleft(prev)

            elif isinstance(prev, NavigableString) and prev.strip():
                items.appendleft(prev)  # prev is a string

            else:
                items.appendleft(prev)
                break  # prev is neither of the above

            prev = prev.previous_sibling
        collections.append(items)
    return collections


def assign_bq_sections(html: BeautifulSoup) -> BeautifulSoup:
    """
    1. Collect blockquotes matching `blockquote_parent` critera
    2. Blockquotes, by themselves, do not provide context
    3. They need to be associated with previous elements
    4. The association is done through `make_partitions`
    5. Each partition is a blockquote with associated elements
    6. For each partition found, wrap a <section> tag around it
    7. Note two deque objects in this process
    8. The first deque itemizes partitions of blockquotes
    9. The second deque itemizes each partition's associated elements
    """

    partitions: deque = make_partitions(html(blockquote_parent))

    while partitions:  # note collection of partition in partitions
        partition: deque = partitions.popleft()  # pop a partition out
        l = partition[-1]  # get the last element in popped partition
        wrap_in_tag("section", l, partition, html)  # wrap the partition
    return html
