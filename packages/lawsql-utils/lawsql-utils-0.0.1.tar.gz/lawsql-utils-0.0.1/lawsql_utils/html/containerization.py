from collections import deque

from bs4 import BeautifulSoup, Tag
from bs4.element import PageElement


def wrap_in_tag(
    tag_name_that_will_wrap: str,
    anchor: BeautifulSoup,
    q: deque,
    html: BeautifulSoup,
) -> None:
    """
    Inputs:
    1. "tag_name_that_will_wrap" representing the tag name to create
    2. start element "anchor"
    3. a queue "q" of items that need to be wrapped / extracted from the source html tree
    4. source html tree to insert the wrapping tag (now extracted)

    Process:
    1. Create a new tag in "html"
    2. Preposition this new tag before the start element "anchor"
    3. For each item in the queue, extract the item from the original "html" tree
    4. This will destroy elements extracted
    5. The extracts can then be collected and reinserted
    6. The reinsertion will occur inside the newly created and prepositioned "anchor"
    """
    # preposition wrapper before anchor
    wrapper = html.new_tag(tag_name_that_will_wrap)
    anchor.insert_before(wrapper)

    # remove prospective wrapees from queue
    extracts = []
    while q:
        item = q.popleft()
        if item is None:
            continue
        extracts.append(item.extract())

    # add wrapees to wrapper
    wrapper.extend(extracts)

    # return modified soup
    return html


def containerize_next(elem: PageElement, html: BeautifulSoup):
    """
    There are strings that do not have parent tags.

    This "containerizes" the string element with a wrapping "p" tag

    Raw, e.g.
    ```html
    <br>
    <br>
    This is a new string that is unwrapped
        <strong>
            but note this emphasized portion
        </strong>
    <br>
    <br>
    ```

    Formatted, e.g.
    ```html
    <br>
    <br>
    <p>
        This is a new string that is unwrapped
            <strong>
                but note this emphasized portion
            </strong>
    </p>
    <br>
    <br>
    ```

    Since the "new string" may be connected to other elements like `<strong>` and `<em>`,
    we need to traverse the siblings of the new string until it reaches an indicator
    of a breakline, e.g. `<br>` / `<p>`.

    Every time a new element is traversed that is not an indicator of a breakline, add to the `deque`.

    All items added will be included in the wrapping function.

    """
    # set the string element as the first item to wrap
    items = deque([elem])

    # while waiting for the breakline indicator, get subsequent items
    while True:
        elem = elem.next_sibling

        if isinstance(elem, Tag) and elem.name == "br":
            break

        elif isinstance(elem, Tag) and elem.name == "p":
            break

        elif not elem:
            break

        else:
            items.append(elem)

    # with a `deque` established, wrap the items in a <p> tag
    return wrap_in_tag("p", items[0], items, html)
