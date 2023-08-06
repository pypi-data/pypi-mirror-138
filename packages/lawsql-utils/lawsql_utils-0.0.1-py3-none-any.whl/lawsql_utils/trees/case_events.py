from typing import NoReturn, Union

REQUIRED_IN_DECISION = ("citation", "action")


def is_decision_event_format(data) -> Union[NoReturn, dict]:
    """Some checks to determine if the data dictionary is valid:
    1. Is it a `dict`?
    2. Has it been given `path` param which maps to a materialized path?
    3. Are _all_ of the required keys - `citation`, `action` and `content` included in the `dict`?
    """

    if not isinstance(data, dict):
        raise Exception(f"Improper formatting - {str(data)}")

    if "path" not in data:
        raise Exception(f"Missing 'path' in - {str(data)}")

    if not all(k for k in data if k in REQUIRED_IN_DECISION):
        raise Exception(f"Required: citation & action. {str(data)}")

    return data


def add_decision_path_to_raw_event(data: dict, path: str) -> dict:
    return {
        "citation": data.get("citation", None),
        "action": data.get("action", None),
        "content": data.get("content", None),
        "path": path,
    }
