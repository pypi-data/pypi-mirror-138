from typing import NoReturn, Optional, Union

ALLOWED_IN_STATUTE = ("locator", "content", "caption")


def is_statutory_event_format(data) -> Union[NoReturn, dict]:
    """Some checks to determine if the data dictionary is valid:
    1. Is it a `dict`?
    2. Has it been given `path` param which maps to a materialized path?
    3. Are any of the allowed keys - `locator`, `content` and `caption` included in the `dict`?
    """

    if not isinstance(data, dict):
        raise Exception(f"Improper formatting - {str(data)}")

    if "path" not in data:
        raise Exception(f"Missing 'path' in - {str(data)}")

    if not any(k for k in data if k in ALLOWED_IN_STATUTE):
        raise Exception(f"Missing: locator, caption or content - {str(data)}")

    return data


def add_statutory_path_to_raw_event(data: dict, path: str) -> dict:
    return {
        "locator": data.get("locator", None),
        "content": data.get("content", None),
        "caption": data.get("caption", None),
        "path": path,
    }
