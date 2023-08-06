import inspect
import json
from pydoc import locate
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple, Type, get_origin

from typeguard import check_type

_KEY_SEPARATOR = '.'
_CLASS_SEPARATOR = ':'
_PARAM_SEPARATOR = '='


def get_nested_dictionary_and_key(
    dictionary: Dict[str, Any],
    name: str,
    set_mode: bool = False,
) -> Tuple[Dict[str, Any], str]:
    *nested_keys, last_key = name.split(_KEY_SEPARATOR)

    key_list = list()
    for key in nested_keys:
        key_list.append(key)
        if key not in dictionary:
            if set_mode:
                dictionary[key] = dict()
            else:
                raise KeyError(f"Param '{_KEY_SEPARATOR.join(key_list)}' is not in dictionary.")

        if not isinstance(dictionary[key], dict):
            if set_mode:
                dictionary[key] = dict()
            else:
                raise ValueError(f"Param '{_KEY_SEPARATOR.join(key_list)}' is not dictionary.")

        dictionary = dictionary[key]

    if not set_mode and last_key not in dictionary:
        raise KeyError(f"Param '{last_key}' is not in dictionary.")

    return dictionary, last_key


def flatten_keys(obj: Any, _prefix: str = "") -> List[str]:
    if not isinstance(obj, dict):
        return [_prefix]

    keys = []
    for k, v in obj.items():
        keys.extend(flatten_keys(v, join_key(_prefix, k)))

    return keys


def check_key_override(key: str, keys: Sequence[str]) -> bool:
    key_parts = key.split(_KEY_SEPARATOR)
    return any(all(k1 == k2 for k1, k2 in zip(key_parts, k.split(_KEY_SEPARATOR))) for k in keys)


def join_key(*args: str) -> str:
    return _KEY_SEPARATOR.join(a for a in args if a)


def join_class(*args: str) -> str:
    return _CLASS_SEPARATOR.join(a for a in args if a)


def parse_class(
    dictionary: Dict[str, Any],
    keyword: str,
) -> Tuple[Dict[str, Any], str, Optional[str]]:
    kwargs = dictionary.copy()
    class_name = kwargs.pop(keyword)
    class_name, _, option = class_name.partition(_CLASS_SEPARATOR)
    return kwargs, class_name, option


def parse_param(param: str) -> Tuple[str, Any]:
    key, separator, raw_value = param.partition(_PARAM_SEPARATOR)

    if not separator:
        raise ValueError(f"Param '{param}' has not assigned value.")

    try:
        value = json.loads(raw_value)
    except json.decoder.JSONDecodeError:
        value = raw_value

    return key, value


def import_class(name: str) -> type:
    cls = locate(name)
    if cls is None:
        raise ValueError(f"Class '{name}' does not exist.")
    if not isinstance(cls, type):
        raise ValueError(f"Object '{name}' is not a class.")
    return cls


def get_class_name(obj: Any) -> str:
    try:
        return obj.__name__
    except AttributeError:
        return obj.__class__.__name__


def get_hints(signature: inspect.Signature) -> Dict[str, Any]:
    type_hints: Dict[str, Any] = {}
    for name, param in signature.parameters.items():
        if param.annotation is not inspect.Parameter.empty:
            param_type = param.annotation
        elif param.default is not inspect.Parameter.empty and param.default is not None:
            param_type = get_origin(param.default) or type(param.default)
        else:
            param_type = Any

        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            type_hints[name] = Tuple[param_type, ...]  # type: ignore
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            type_hints[name] = Dict[str, param_type]  # type: ignore
        else:
            type_hints[name] = param_type

    return type_hints


def check_params_name_override(
    location: str,
    params: Dict[str, Any],
    kwargs: Dict[str, Any],
) -> None:
    if overrides := set(params).intersection(kwargs):
        raise ValueError(f"Override {location}'s class arguments {overrides}.")


def check_missing_values(
    location: str,
    kwargs: Dict[str, Any],
    missing_value: str,
) -> None:
    for name, value in kwargs.items():
        if isinstance(value, str) and value.endswith(missing_value):
            raise ValueError(f"Missing {location}'s class argument '{name}' value.")


def check_params_type(
    location: str,
    cls: Type[Any],
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> None:
    signature = inspect.signature(cls)
    try:
        arguments = signature.bind(*args, **kwargs).arguments
    except TypeError as e:
        raise TypeError(f"The {location}'s class {''.join(e.args)}.")

    for name, expected_type in get_hints(signature).items():
        if name in arguments:
            try:
                check_type(
                    argname=f"{location}'s class argument '{name}'",
                    value=arguments[name],
                    expected_type=expected_type,
                )
            except TypeError as e:
                raise TypeError(f"The {''.join(e.args)}.")


def convert_to_primitive_types(obj: Any, missing_value: str) -> Any:
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj

    if isinstance(obj, Mapping):
        return {
            convert_to_primitive_types(k, missing_value): convert_to_primitive_types(
                v, missing_value
            )
            for k, v in obj.items()
        }

    if isinstance(obj, Sequence):
        return [convert_to_primitive_types(item, missing_value) for item in obj]

    return missing_value
