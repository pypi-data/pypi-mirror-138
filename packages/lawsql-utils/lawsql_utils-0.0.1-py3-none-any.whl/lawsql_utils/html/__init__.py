from .containerization import containerize_next, wrap_in_tag
from .footnotes import (
    get_asterisk_from_fn_pattern,
    get_digit_from_fn_pattern,
    get_just_integers,
    get_pure_digit_key_from_sup_tag,
    get_sup_tags,
    remove_footnotes,
)
from .formatting import (
    extract_text_if_html,
    identify_tags,
    make_soup,
    make_soup_get_italicized,
    make_soup_xaoless,
    soup_xaoless,
)
