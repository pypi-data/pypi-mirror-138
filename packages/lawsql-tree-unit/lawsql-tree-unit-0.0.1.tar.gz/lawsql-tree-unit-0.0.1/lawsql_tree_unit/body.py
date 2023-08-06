from pathlib import Path

from lawsql_utils.files import load_yaml_list

from .unformatted import (
    fix_absent_signer_problem,
    fix_multiple_sections_in_first,
)


def set_units(folder: Path, data: dict):
    """
    If a preformatted file exists, i.e. data sourced from the old nightshade "Republic Act" repository,
    or formatted manually for use (see rawlaw repository), use the data contained in this file. The file is uniformly named as follows: `category` + `serial_number`.`yaml`, e.g. `ra11054.yaml` for Republic Act No. 11054;

    If a preformatted file is absent,  use the unformatted `units.yaml` file contained within the statute folder. The contents of this file is contained
    in the data dictionary passed.

    Args:
        folder (Path): [description]
        data (dict): [description]

    Returns:
        [type]: [description]
    """
    if (pre := folder / f"{data['category']}{folder.parts[-1]}.yaml").exists():
        print(f"Provisions found (preformatted): {pre}.")
        data["units"] = load_yaml_list(pre)

    elif (unformatted := folder / "units.yaml").exists():
        print(f"Provisions found (unformatted): {unformatted}.")
        data["units"] = load_yaml_list(unformatted)
        data = fix_absent_signer_problem(data)
        data = fix_multiple_sections_in_first(data)

    else:
        print(f"No units found in {folder}")
    return data
