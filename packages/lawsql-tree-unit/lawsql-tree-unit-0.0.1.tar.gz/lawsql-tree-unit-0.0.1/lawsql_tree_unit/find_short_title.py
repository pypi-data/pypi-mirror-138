import re
from typing import Optional

from lawsql_utils.trees import data_tree_walker


def get_first_short_title_from_units(data_with_units: dict) -> Optional[str]:
    if not "units" in data_with_units:
        return None
    l = list(data_tree_walker(data_with_units, "short_title"))
    return l[0] if l else None


def extract_quoted_pattern(text: str):
    if match_found := re.compile(r'".*"').search(text):
        return match_found.group().strip('".')
    return "Short title indicators but no quoted pattern found."


def has_title_content(text: str):
    patterns = [
        r"""(
            ^
            (This|The)
            \s*
            (Act|Code)
            \s*
            (may|shall)
            \s*
            be
            \s*
            (cited|known)
        )""",
        r"""(
            ^
            The
            \s*
            short
            \s*
            title
            \s*
            of
            \s*
            this
            \s*
            (Act|Code)
            \s*
            shall
            \s*
            be
        )""",
    ]
    return re.compile("|".join(patterns), re.X | re.I).search(text.strip())


def has_title_caption(node: dict):
    return (x := node.get("caption", None)) and is_short_title_caption(x)


def is_short_title_caption(text: str):
    return re.compile(r"short\s*title", re.I).search(text)


def can_extract_short(node, content):
    return has_title_caption(node) or has_title_content(content)


def short_title_found(node: dict) -> bool:
    if not (content := node.get("content", None)):
        return False
    if not can_extract_short(node, content):
        return False
    return True
