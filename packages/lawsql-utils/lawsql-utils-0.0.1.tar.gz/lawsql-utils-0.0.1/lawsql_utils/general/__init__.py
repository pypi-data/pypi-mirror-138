from .combine_iterators import concat_iterators
from .patterns import (
    construct_indicators,
    get_first_matching_text_of_regex,
    helper_test_match,
    if_match_found_return_text,
    remove_pattern_if_found_else_text,
    text_in_pattern_count,
)
from .regex_constructors import (
    combine_regexes_as_options,
    construct_acronyms,
    construct_negative_lookbehinds,
    construct_prefix_options,
)
from .text_helpers import (
    format_full_date,
    get_splits_from_slicer,
    parse_date_if_exists,
    trim_text,
)
