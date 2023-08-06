import inspect
from pydoc import locate
from typing import Any, Sequence, get_origin


def get_nested(
    dictionary: dict[str, Any],
    name: str,
    set_mode: bool = False,
    separator: str = '.',
) -> tuple[dict[str, Any], str]:
    *nested_keys, last_key = name.split(separator)

    key_list = list()
    for key in nested_keys:
        key_list.append(key)
        if key not in dictionary:
            if set_mode:
                dictionary[key] = dict()
            else:
                raise KeyError(f"Param '{separator.join(key_list)}' is not in dictionary.")

        if not isinstance(dictionary[key], dict):
            if set_mode:
                dictionary[key] = dict()
            else:
                raise ValueError(f"Param '{separator.join(key_list)}' is not dictionary.")

        dictionary = dictionary[key]

    if not set_mode and last_key not in dictionary:
        raise KeyError(f"Param '{last_key}' is not in dictionary.")

    return dictionary, last_key


def import_class(name: str) -> type:
    cls = locate(name)
    if cls is None:
        raise ValueError(f"Class '{name}' does not exist.")
    if not isinstance(cls, type):
        raise ValueError(f"Object '{name}' is not a class.")
    return cls


def get_name(obj: Any) -> str:
    try:
        return obj.__name__
    except AttributeError:
        return obj.__class__.__name__


def get_hints(signature: inspect.Signature) -> dict[str, Any]:
    type_hints: dict[str, Any] = {}
    for name, param in signature.parameters.items():
        if param.annotation is not inspect.Parameter.empty:
            param_type = param.annotation
        elif param.default is not inspect.Parameter.empty and param.default is not None:
            param_type = get_origin(param.default) or type(param.default)
        else:
            param_type = Any

        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            type_hints[name] = tuple[param_type, ...]  # type: ignore
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            type_hints[name] = dict[str, param_type]  # type: ignore
        else:
            type_hints[name] = param_type

    return type_hints


def check_key_in_flatten_keys(key: str, flatten_keys: Sequence[str], separator: str) -> bool:
    key_parts = key.split(separator)
    return any(all(k1 == k2 for k1, k2 in zip(key_parts, k.split(separator))) for k in flatten_keys)
