import inspect
import sys
import warnings
from pathlib import Path
from typing import (
    Any,
    Callable,
    Generic,
    Mapping,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
)

import yaml
from typeguard import check_type
from yaml import YAMLError

from smartparams.cli import parse_arguments
from smartparams.io import load, to_string
from smartparams.utils import (
    check_key_in_flatten_keys,
    get_hints,
    get_name,
    get_nested,
    import_class,
)

_T = TypeVar("_T")


class Smart(Generic[_T]):
    name = "Smart"
    keyword = "class"
    missing_value = '???'

    key_separator = '.'
    param_separator = '='
    class_separator = ':'

    default_print_format = 'yaml'

    check_missings: Optional[bool] = None
    check_typings: Optional[bool] = None
    check_overrides: Optional[bool] = None

    _location = '__root__'
    _allow_only_registered = False
    _aliases: dict[str, str] = dict()
    _origins: dict[str, str] = dict()

    def __init__(self, _class: Optional[Type[_T]] = None, /, **params: Any) -> None:
        self._class = _class
        self._params = params

    @property
    def type(self) -> Optional[Type[_T]]:
        return self._class

    @property
    def params(self) -> dict[str, Any]:
        return self._params.copy()

    @classmethod
    def register(
        cls,
        classes: Union[Sequence[str], Mapping[str, str]],
        allow_only_registered: Optional[bool] = None,
    ) -> Type['Smart']:
        if allow_only_registered:
            cls._allow_only_registered = True
        elif allow_only_registered is False and cls._allow_only_registered:
            warnings.warn("Cannot disallow only registered classes if already allowed.")

        if isinstance(classes, Sequence):
            cls._register_classes(classes)
        elif isinstance(classes, Mapping):
            cls._register_aliases(classes)
        else:
            raise TypeError(f"Register classes type '{type(classes)}' is not supported.")

        return cls

    def __call__(self, *args: Any, **kwargs: Any) -> _T:
        if self._class is None:
            raise AttributeError("Class is not set.")

        return self._check_and_init_class(
            location=self._location,
            cls=self._class,
            args=args,
            kwargs=kwargs,
            params=self._instantiate(self._params, self._location),
        )

    def __str__(self) -> str:
        if self._class is None:
            return f"{self.name}({str(self._params)})"

        params = ", ".join((f"{k}={v}" for k, v in self._params.items()))
        return f"{get_name(self._class)}:{self.name}({params})"

    def __repr__(self) -> str:
        return str(self)

    def keys(self) -> list[str]:
        return list(self._params)

    def flatten_keys(self) -> list[str]:
        return self._flatten_keys(self._params)

    def get(self, name: str, init: bool = False, persist: bool = True) -> Any:
        dictionary, key = get_nested(
            dictionary=self._params,
            name=name,
            set_mode=False,
            separator=self.key_separator,
        )

        if init:
            obj = self._instantiate(dictionary[key], self._location)
            if persist:
                dictionary[key] = obj
            return obj

        return dictionary[key]

    def set(self, name: str, value: Any) -> Any:
        dictionary, key = get_nested(
            dictionary=self._params,
            name=name,
            set_mode=True,
            separator=self.key_separator,
        )
        dictionary[key] = value
        return value

    def pop(self, name: str, init: bool = False) -> Any:
        dictionary, key = get_nested(
            dictionary=self._params,
            name=name,
            set_mode=False,
            separator=self.key_separator,
        )
        value = dictionary.pop(key)
        if init:
            return self._instantiate(value, self._location)
        return value

    def map(self, name: str, function: Callable) -> Any:
        dictionary, key = get_nested(
            dictionary=self._params,
            name=name,
            set_mode=False,
            separator=self.key_separator,
        )
        dictionary[key] = value = function(dictionary[key])
        return value

    def update(
        self,
        source: Union['Smart', dict[str, Any], list[str], Path],
        override: bool = True,
    ) -> 'Smart':
        if isinstance(source, Smart):
            self._update_from_smart(source, override)
        elif isinstance(source, dict):
            self._update_from_dict(source, override)
        elif isinstance(source, list):
            self._update_from_list(source, override)
        elif isinstance(source, Path):
            self._update_from_path(source, override)
        else:
            raise TypeError(f"Source type '{type(source)}' is not supported.")

        return self

    def run(
        self,
        function: Optional[Callable] = None,
        path: Optional[Path] = None,
        dump: bool = False,
        save: bool = False,
    ) -> 'Smart':
        args = parse_arguments(
            path=path,
            dump=dump,
            save=save,
        )

        if args.path and args.path.exists():
            self.update(args.path)

        self.update(args.params)

        if args.dump:
            self._dump(
                path=args.path,
                save=args.save,
            )
        elif function is None:
            self()
        else:
            function(self)

        return self

    @classmethod
    def _register_classes(cls, classes: Sequence[str]) -> None:
        cls._register_aliases({item: item for item in classes})

    @classmethod
    def _register_aliases(cls, aliases: Mapping[str, str]) -> None:
        for origin, alias in aliases.items():
            if origin in cls._aliases:
                warnings.warn(f"Origin '{origin}' has been overridden.")
                cls._origins.pop(cls._aliases.pop(origin))

            if alias in cls._origins:
                warnings.warn(f"Alias '{alias}' has been overridden.")
                cls._aliases.pop(cls._origins.pop(alias))

            cls._aliases[origin] = alias
            cls._origins[alias] = origin

    def _representation(self, obj: Any, skip_default: bool = False) -> dict[str, Any]:
        representation: dict[str, Any] = dict()
        signature = inspect.signature(obj)

        for name, param in signature.parameters.items():
            if name != 'self' and param.kind in (
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            ):
                annotation = param.annotation
                default = param.default

                if annotation is Smart or isinstance(default, Smart) and default.type is None:
                    representation[name] = {
                        self.keyword: self.name,
                    }
                elif get_origin(annotation) is Smart or isinstance(default, Smart):
                    if isinstance(default, Smart):
                        param_type = default.type
                    else:
                        param_type, *_ = get_args(annotation)

                    keyword = inspect.formatannotation(param_type)
                    keyword = self._aliases.get(keyword, keyword)
                    keyword = keyword + self.class_separator + self.name

                    representation[name] = {
                        self.keyword: keyword,
                        **self._representation(param_type, skip_default),
                    }
                elif default is not inspect.Parameter.empty and skip_default:
                    continue
                elif default is None or isinstance(default, (bool, float, int, str)):
                    representation[name] = default
                elif annotation is not inspect.Parameter.empty and isinstance(annotation, type):
                    if annotation in (bool, float, int, str):
                        representation[name] = annotation.__name__ + self.missing_value
                    else:
                        keyword = inspect.formatannotation(annotation)
                        keyword = self._aliases.get(keyword, keyword)
                        representation[name] = {
                            self.keyword: keyword,
                            **self._representation(annotation, skip_default),
                        }
                else:
                    representation[name] = self.missing_value

        return representation

    def _flatten_keys(self, obj: Any, prefix: str = "") -> list[str]:
        if not isinstance(obj, dict):
            return [prefix]

        keys = []
        for k, v in obj.items():
            if prefix:
                k = prefix + self.key_separator + k
            keys.extend(self._flatten_keys(v, k))

        return keys

    def _update_from_smart(self, smart: 'Smart', override: bool) -> None:
        flatten_keys = self.flatten_keys()
        for key in smart.flatten_keys():
            if override or not check_key_in_flatten_keys(key, flatten_keys, self.key_separator):
                self.set(key, smart.get(key))

    def _update_from_dict(self, params: dict[str, Any], override: bool) -> None:
        self._update_from_smart(Smart(**params), override)

    def _update_from_list(self, params_list: list[str], override: bool) -> None:
        smart: Smart = Smart()
        for param in params_list:
            key, separator, raw_value = param.partition(self.param_separator)

            if not separator:
                raise ValueError(f"Param '{param}' does not contain '=' separator.")

            try:
                value = yaml.safe_load(raw_value)
            except YAMLError as e:
                raise ValueError(f"Param '{param}' has invalid value.") from e

            smart.set(key, value)

        self._update_from_smart(smart, override)

    def _update_from_path(self, path: Path, override: bool) -> None:
        self._update_from_dict(load(path), override)

    def _instantiate(self, obj: Any, _location: str = '') -> Any:
        location = _location or self._location

        if isinstance(obj, dict):
            if self.keyword in obj:
                return self._instantiate_class(obj, location)

            return self._instantiate_dict(obj, location)

        if isinstance(obj, list):
            return self._instantiate_list(obj, location)

        return obj

    def _instantiate_dict(self, dictionary: dict[str, Any], location: str) -> dict[str, Any]:
        return {
            key: self._instantiate(value, f"{location}{self.key_separator}{key}")
            for key, value in dictionary.items()
        }

    def _instantiate_list(self, lst: list[Any], location: str) -> list[Any]:
        return [
            self._instantiate(element, f"{location}{self.key_separator}{index}")
            for index, element in enumerate(lst)
        ]

    def _instantiate_class(self, dictionary: dict[str, Any], location: str) -> Any:
        kwargs = dictionary.copy()
        class_name = kwargs.pop(self.keyword)
        class_name, _, option = class_name.partition(self.class_separator)

        if class_name == self.name:
            return self._check_and_init_class(
                location=location,
                cls=Smart,
                kwargs=kwargs,
            )

        if class_name in self._origins:
            class_name = self._origins[class_name]
        elif self._allow_only_registered:
            raise ImportError(f"Class '{class_name}' is not registered.")

        cls = cast(Type[_T], import_class(class_name))

        if option:
            if option == self.name:
                return self._check_and_init_class(
                    location=location,
                    cls=Smart,
                    args=(cls,),
                    kwargs=kwargs,
                )
            else:
                raise ValueError(f"Option '{option}' is not supported.")
        else:
            return self._check_and_init_class(
                location=location,
                cls=cls,
                kwargs=kwargs,
            )

    def _check_and_init_class(
        self,
        location: str,
        cls: Type[Any],
        args: Optional[tuple[Any, ...]] = None,
        kwargs: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> Any:
        location_with_classname = f"{location}{self.class_separator}{get_name(cls)}"
        args = args or tuple()
        kwargs = kwargs or dict()

        if params:
            if self.check_overrides is not False:
                self._check_overrides(
                    params=params,
                    kwargs=kwargs,
                    location=location_with_classname,
                )

            params = params.copy()
            params.update(kwargs)
            kwargs = params

        if self.check_missings is not False:
            self._check_missings(
                kwargs=kwargs,
                location=location_with_classname,
            )

        if self.check_typings is not False:
            self._check_typings(
                cls=cls,
                args=args,
                kwargs=kwargs,
                location=location_with_classname,
            )

        try:
            obj = cls(*args, **kwargs)
        except Exception as e:
            raise RuntimeError(f"Error during instantiate {location_with_classname} class.") from e
        else:
            if isinstance(obj, Smart):
                obj._location = location
            return obj

    def _check_overrides(
        self,
        location: str,
        params: dict[str, Any],
        kwargs: dict[str, Any],
    ) -> None:
        if overrides := set(params).intersection(kwargs):
            msg = f"Override {location}'s class arguments {overrides}."
            if self.check_overrides:
                raise ValueError(msg)
            warnings.warn(msg)

    def _check_missings(
        self,
        location: str,
        kwargs: dict[str, Any],
    ) -> None:
        for name, value in kwargs.items():
            if isinstance(value, str) and value.endswith(self.missing_value):
                msg = f"Missing {location}'s class argument '{name}' value."
                if self.check_missings:
                    raise ValueError(msg)
                warnings.warn(msg)

    def _check_typings(
        self,
        location: str,
        cls: Type[Any],
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> None:
        signature = inspect.signature(cls)
        arguments = signature.bind(*args, **kwargs).arguments

        for name, expected_type in get_hints(signature).items():
            if name in arguments:
                try:
                    check_type(
                        argname=f"{location}'s class argument '{name}'",
                        value=arguments[name],
                        expected_type=expected_type,
                    )
                except TypeError as e:
                    msg = f"The {''.join(e.args)}."
                    if self.check_typings:
                        raise TypeError(msg)
                    warnings.warn(msg)

    def _dump(self, path: Optional[Path], save: bool) -> None:
        self.update(
            self._representation(self._class, skip_default=bool(self._params)),
            override=False,
        )

        print_format = path.suffix.strip('.') if path else self.default_print_format
        text_params = to_string(self.params, print_format)
        text_keys = to_string(self.flatten_keys(), print_format)

        print(f"{text_params}---\n{text_keys}")

        if save:
            if path:
                path.write_text(text_params)
                print(f"Params saved in {path}.")
            else:
                print("Cannot save if path is not specified.", file=sys.stderr)
