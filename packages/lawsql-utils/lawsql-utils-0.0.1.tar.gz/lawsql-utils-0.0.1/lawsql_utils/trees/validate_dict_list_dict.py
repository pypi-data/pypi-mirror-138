from typing import Iterator, Optional


def dict_key_with_list_of_dicts(
    key: str,
    data: Optional[dict] = None,
) -> Optional[Iterator[dict]]:
    """
    If a `data` dictionary is passed, check if it contains the given `key`;
    If yes, determine if the contents of the dictionary is a list instance;
    If yes, determine yield each item that consists of a dictionary;
    If an item is not a dictionary, raise exception.
    """
    if not data:
        return None
    if not (found := data.get(key, None)):
        return None
    if not (isinstance(found, list)):
        raise Exception(f"Must be a list: {key=} | {data=}")
    for data_item in found:
        if isinstance(data_item, dict):
            yield data_item
        else:
            raise Exception(f"Must be a dictionary in the list | {data=}")
