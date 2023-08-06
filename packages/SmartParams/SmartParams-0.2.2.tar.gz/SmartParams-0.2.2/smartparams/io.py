from pathlib import Path
from typing import Any

import yaml


def to_string(data: Any, fmt: str) -> str:
    if fmt in ('yml', 'yaml'):
        return yaml.safe_dump(
            data=data,
            sort_keys=False,
        )

    raise ValueError(f"Format '{fmt}' is not supported.")


def load(path: Path) -> dict[str, Any]:
    if not path.suffix:
        raise ValueError(f"File '{path}' has no extension.")
    elif path.suffix in ('.yml', '.yaml'):
        with path.open() as stream:
            dictionary = yaml.safe_load(stream)
    else:
        raise ValueError(f"File extension '{path.suffix}' is not supported.")

    if isinstance(dictionary, dict):
        return dictionary
    if dictionary is None:
        return dict()
    raise ValueError(f"File '{path}' does not contain a dictionary.")
