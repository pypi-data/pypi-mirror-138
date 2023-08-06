from pathlib import Path
from typing import Any, Dict

import yaml

_YAML_SUFFIXES = ('yaml', 'yml', '.yaml', '.yml')


def load_data(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"File '{path}' does not exist.")

    if not path.suffix:
        raise ValueError(f"File '{path}' has no extension.")
    elif path.suffix in _YAML_SUFFIXES:
        with path.open() as stream:
            dictionary = yaml.safe_load(stream)
    else:
        raise ValueError(f"File extension '{path.suffix}' is not supported.")

    if isinstance(dictionary, dict):
        return dictionary
    if dictionary is None:
        return dict()
    raise ValueError(f"File '{path}' does not contain a dictionary.")


def print_data(data: Any, fmt: str) -> None:
    if fmt in _YAML_SUFFIXES:
        data = yaml.safe_dump(
            data=data,
            sort_keys=False,
        )
    else:
        raise ValueError(f"Format '{fmt}' is not supported.")

    print(data)


def save_data(data: Dict[str, Any], path: Path) -> None:
    if not path.suffix:
        raise ValueError(f"File '{path}' has no extension.")

    if path.suffix in _YAML_SUFFIXES:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w') as stream:
            yaml.safe_dump(
                data=data,
                stream=stream,
                sort_keys=False,
            )
    else:
        raise ValueError(f"File extension '{path.suffix}' is not supported.")
