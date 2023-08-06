import re
from pathlib import Path
from typing import NoReturn, Union

from lawsql_utils.general import trim_text
from markdown2 import Markdown

from .body import set_units
from .extract_details import extract_details
from .find_short_title import extract_quoted_pattern, short_title_found

markdowner = Markdown(..., extras=["tables", "markdown-in-html"])

MAX_ITEM = 500  # creation of unit item labels
MAX_CAPTION = 1000  # creation of unit caption labels


def format_doc_content(nodes: list[dict]):
    """
    1. Recursive constraint for nested units to comply with constraints;
    2. Applicable to Document containers.
    """
    for node in nodes:
        if content := node.get("content", None):
            node["content"] = markdowner.convert(content).strip()
        if node.get("units", None):
            format_doc_content(node["units"])  # call self


def format_units(nodes: list[dict]) -> None:
    """
    1. Recursive constraint for nested units to comply with constraints;
    2. Creates `short_title` key if found in a particular node.
    3. Applicable to Statute / Codification containers.
    """
    for node in nodes:
        if item := node.get("item", None):
            node["item"] = trim_text(make_uniform_section(str(item)), MAX_ITEM)

        if caption := node.get("caption", None):
            node["caption"] = trim_text(str(caption), MAX_CAPTION)

        if content := node.get("content", None):
            if short_title_found(node):
                node["short_title"] = extract_quoted_pattern(node["content"])
            node["content"] = markdowner.convert(content).strip()

        if node.get("units", None):
            format_units(node["units"])  # call self


def load_data(loc: Path) -> Union[dict, NoReturn]:
    """With the passed directory, get the relevant files.

    The following files in the directory, i.e. ("pd1") are processed, if they exist

    1. `details.yaml`
    2. `extra.html`
    3. `units.yaml` (unformatted)
    4. `pd1.yaml` (preformatted Presidential Decree No. 1)

    This function combines the contents of the `details.yaml` file
    with the contents of either the `units.yaml` file or the `pd1.yaml` file.
    The resulting combination is a dictionary of key value pairs.

    Args:
        loc (Path): The source directory of the files mentioned above.

    Returns:
        Optional[dict]: The combined data found in the folder.
    """
    if not (data := extract_details(loc)):
        raise Exception(f"No details.yaml file: {loc}.")

    return set_units(loc, data)


def make_uniform_section(raw: str):
    """Replace the SECTION | SEC. | Sec. format with the word Section, if applicable."""
    regex = r"""
        ^\s*
        S
        (
            ECTION|
            EC|
            ec
        )
        [\s.,]+
    """
    pattern = re.compile(regex, re.X)
    if pattern.search(raw):
        text = pattern.sub("Section ", raw)
        text = text.strip("., ")
        return text
    return raw
