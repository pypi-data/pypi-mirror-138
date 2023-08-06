def remove_empty_children_nodes(items: list[dict]) -> None:
    """Recursively remove empty children from the tree

    Args:
        items (list[dict]): The list of nested dicts
    """
    for i in items:
        i.pop("path", None)
        if i.get("children", None):
            remove_empty_children_nodes(i["children"])
        else:
            i.pop("children", None)


def clean_json(json_data: dict) -> dict:
    """Remove empty children values

    Args:
        json_data (dict): Assumes a nested dictionary with "children" keys

    Returns:
        dict: The same nested dictionary with empty "children" keys removed
    """
    #
    if json_data.get("children", None):
        remove_empty_children_nodes(json_data["children"])
    return json_data
