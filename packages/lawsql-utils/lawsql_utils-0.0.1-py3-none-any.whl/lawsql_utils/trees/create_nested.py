from .clear_nested import clean_json


def add_path_to_parent(unit: dict, parent: dict) -> None:
    """Recursive function to generate branches from the parent dictionary

    Requires:
    1. Materialized path regime with four character internvals
    2. Initialized "children" key to indicate child nodes of the given `unit`

    Args:
        unit (dict): Present element processed by recursive call
        res (dict): The resulting dictionary
    """

    # initialize the children field (if it does not exist)
    if not parent.get("children"):
        parent["children"] = []

    # retrieve the parent path
    parent_path = parent["path"]

    # get the unit path
    # each path-level consists of 4 characters as default for treebeard;
    # slice the four characters of the path to get parent of the unit
    parent_path_of_unit = unit["path"][:-4]

    # for each unit that is processed, check if they have the same parent
    # if they have the same parent, add to the "children" key
    # otherwise, for each children key, re-initialize a new branch
    if parent_path_of_unit == parent_path:
        parent["children"].append(unit)
    else:
        for c in parent["children"]:
            add_path_to_parent(unit, c)


def created_nested_json_tree_from_materialized_paths(
    materialized_path_list: list[dict],
) -> dict:
    """
    The first item in list should be root of the tree.

    This first item will be populated with children nodes until the list is exhausted.

    This construct imagines generated queryset values from the Materialized Path from Treebeard, e.g.
    u = Unit.get_root_nodes()[0]
    list(Unit.get_tree(parent=u).values("id", "path", "item", "caption", "content"))

    Args:
        paths (list[dict]): Each list of dicts passed should contain a materialized path, e.g. 00001223, 0000 is the parent of child 00001223

    Returns:
        dict: The root dict which has been populated by the list, with empty "children" nodes removed
    """
    for path in materialized_path_list[1:]:
        add_path_to_parent(path, materialized_path_list[0])
    return clean_json(materialized_path_list[0])
