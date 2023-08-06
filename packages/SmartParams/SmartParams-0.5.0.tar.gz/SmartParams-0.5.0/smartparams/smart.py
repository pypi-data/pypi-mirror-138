import inspect
from copy import deepcopy
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
)

from smartparams.cli import Print, parse_arguments
from smartparams.io import load_data, print_data, save_data
from smartparams.utils import (
    check_key_override,
    check_missing_values,
    check_params_name_override,
    check_params_type,
    convert_to_primitive_types,
    flatten_keys,
    get_class_name,
    get_nested_dictionary_and_key,
    import_class,
    join_class,
    join_key,
    parse_class,
    parse_param,
)

_T = TypeVar('_T')


class Smart(Generic[_T]):
    def __init__(self, _class: Optional[Type[_T]] = None, /, **params: Any) -> None:
        self._class = _class
        self._params = params

        self._keyword = 'class'
        self._missing_value = '???'

        self._location = ''

        self._check_missings = True
        self._check_typings = True
        self._check_overrides = True

        self._allow_only_registered = False

        self._aliases: Dict[str, str] = dict()
        self._origins: Dict[str, str] = dict()

    @property
    def type(self) -> Optional[Type[_T]]:
        return self._class

    @property
    def params(self) -> Dict[str, Any]:
        return deepcopy(self._params)

    def __call__(self, *args: Any, **kwargs: Any) -> _T:
        if self._class is None:
            raise AttributeError("Class is not set.")

        params = self._instantiate_dict(self._params, self._location)

        if self._check_overrides:
            check_params_name_override(
                params=params,
                kwargs=kwargs,
                location=join_class(self._location, get_class_name(self._class)),
            )

        params.update(kwargs)

        return self._check_and_instantiate_class(
            location=self._location,
            cls=self._class,
            args=args,
            kwargs=params,
        )

    def __str__(self) -> str:
        cls_str = "" if self._class is None else f"[{get_class_name(self._class)}]"
        params_str = ", ".join((f"{k}={v}" for k, v in self._params.items()))
        return f"{self.__class__.__name__}{cls_str}({params_str})"

    def __repr__(self) -> str:
        return str(self)

    def keys(self) -> List[str]:
        return list(self._params)

    def flatten_keys(self) -> List[str]:
        return flatten_keys(self._params)

    def get(self, name: str, init: bool = False, persist: bool = True) -> Any:
        dictionary, key = get_nested_dictionary_and_key(
            dictionary=self._params,
            name=name,
        )

        if init:
            obj = self._instantiate(dictionary[key], self._location)
            if persist:
                dictionary[key] = obj
            return obj

        return dictionary[key]

    def set(self, name: str, value: Any) -> Any:
        dictionary, key = get_nested_dictionary_and_key(
            dictionary=self._params,
            name=name,
            set_mode=True,
        )
        dictionary[key] = value
        return value

    def pop(self, name: str, init: bool = False) -> Any:
        dictionary, key = get_nested_dictionary_and_key(
            dictionary=self._params,
            name=name,
        )
        value = dictionary.pop(key)
        if init:
            return self._instantiate(value, self._location)
        return value

    def map(self, name: str, function: Callable) -> Any:
        dictionary, key = get_nested_dictionary_and_key(
            dictionary=self._params,
            name=name,
        )
        dictionary[key] = value = function(dictionary[key])
        return value

    def update(
        self,
        source: Union['Smart', Dict[str, Any], List[str], Path],
        name: Optional[str] = None,
        override: bool = True,
    ) -> 'Smart':
        if isinstance(source, Smart):
            self._update_from_smart(
                smart=source,
                name=name,
                override=override,
            )
        elif isinstance(source, dict):
            self._update_from_dict(
                params=source,
                name=name,
                override=override,
            )
        elif isinstance(source, list):
            self._update_from_list(
                params_list=source,
                name=name,
                override=override,
            )
        elif isinstance(source, Path):
            self._update_from_path(
                path=source,
                name=name,
                override=override,
            )
        else:
            raise TypeError(f"Source type '{type(source)}' is not supported.")

        return self

    def representation(
        self,
        skip_defaults: bool = False,
        merge_params: bool = False,
    ) -> Dict[str, Any]:
        smart: Smart = Smart()

        if merge_params:
            smart.update(self)

        smart.update(
            source=self._representation(self._class, skip_default=skip_defaults),
            override=False,
        )

        return convert_to_primitive_types(
            obj=smart.params,
            missing_value=self._missing_value,
        )

    def register(self, classes: Union[Sequence[str], Mapping[str, str]]) -> 'Smart':
        if self._location:
            msg = f"Classes can only be registered in root Smart object, not in {self._location}."
            raise AttributeError(msg)

        if isinstance(classes, Sequence):
            self._register_classes(classes)
        elif isinstance(classes, Mapping):
            self._register_aliases(classes)
        else:
            raise TypeError(f"Register classes type '{type(classes)}' is not supported.")

        return self

    def run(
        self,
        function: Callable[['Smart'], Any],
        path: Path = Path('params.yaml'),
    ) -> 'Smart':
        args = parse_arguments(default_path=path)

        if args.path.is_file():
            self.update(args.path)

        self.update(args.params)

        if args.dump:
            save_data(
                data=self.representation(args.skip_defaults, args.merge_params),
                path=args.path,
            )
        elif args.print:
            if args.print == Print.PARAMS:
                print_data(
                    data=self.representation(args.skip_defaults, args.merge_params),
                    fmt=args.format,
                )
            elif args.print == Print.KEYS:
                print_data(
                    data=self.flatten_keys(),
                    fmt=args.format,
                )
            else:
                raise NotImplementedError(f"Print '{args.print}' has not been implemented yet.")
        else:
            function(self)

        return self

    def configurate(
        self,
        *,
        keyword: Optional[str] = None,
        missing_value: Optional[str] = None,
        location: Optional[str] = None,
        check_missings: Optional[bool] = None,
        check_typings: Optional[bool] = None,
        check_overrides: Optional[bool] = None,
        allow_only_registered: Optional[bool] = None,
    ) -> 'Smart':
        if keyword is not None:
            self._keyword = keyword
        if missing_value is not None:
            self._missing_value = missing_value

        if location is not None:
            self._location = location

        if check_missings is not None:
            self._check_missings = check_missings
        if check_typings is not None:
            self._check_typings = check_typings
        if check_overrides is not None:
            self._check_overrides = check_overrides

        if allow_only_registered is not None:
            if allow_only_registered:
                self._allow_only_registered = True
            elif self._allow_only_registered:
                raise AttributeError("Cannot disallow only registered classes if already allowed.")

        return self

    def _update_from_smart(
        self,
        smart: 'Smart',
        name: Optional[str],
        override: bool,
    ) -> None:
        if name is None:
            _flatten_keys = self.flatten_keys()
            for key in smart.flatten_keys():
                if override or not check_key_override(key, _flatten_keys):
                    self.set(key, smart.get(key))
        else:
            try:
                self.update(
                    source=smart.get(name),
                    override=override,
                )
            except Exception as e:
                raise RuntimeError(f"Cannot update with source name '{name}'. " + ' '.join(e.args))

    def _update_from_dict(
        self,
        params: Dict[str, Any],
        name: Optional[str],
        override: bool,
    ) -> None:
        self._update_from_smart(
            smart=Smart(**params),
            name=name,
            override=override,
        )

    def _update_from_list(
        self,
        params_list: List[str],
        name: Optional[str],
        override: bool,
    ) -> None:
        smart: Smart = Smart()
        for param in params_list:
            key, value = parse_param(param)
            smart.set(key, value)

        self._update_from_smart(
            smart=smart,
            name=name,
            override=override,
        )

    def _update_from_path(
        self,
        path: Path,
        name: Optional[str],
        override: bool,
    ) -> None:
        self._update_from_dict(
            params=load_data(path),
            name=name,
            override=override,
        )

    def _instantiate(self, obj: Any, location: str) -> Any:
        if isinstance(obj, dict):
            if self._keyword in obj:
                return self._instantiate_class(obj, location)

            return self._instantiate_dict(obj, location)

        if isinstance(obj, list):
            return self._instantiate_list(obj, location)

        return obj

    def _instantiate_dict(self, dictionary: Dict[str, Any], location: str) -> Dict[str, Any]:
        return {
            key: self._instantiate(value, join_key(location, key))
            for key, value in dictionary.items()
        }

    def _instantiate_list(self, lst: List[Any], location: str) -> List[Any]:
        return [
            self._instantiate(element, join_key(location, str(index)))
            for index, element in enumerate(lst)
        ]

    def _instantiate_class(self, dictionary: Dict[str, Any], location: str) -> Any:
        kwargs, class_name, option = parse_class(dictionary, self._keyword)

        if class_name == self.__class__.__name__:
            return self._check_and_instantiate_class(
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
            if option == self.__class__.__name__:
                return self._check_and_instantiate_class(
                    location=location,
                    cls=Smart,
                    args=(cls,),
                    kwargs=kwargs,
                )
            else:
                raise ValueError(f"Option '{option}' is not supported.")
        else:
            return self._check_and_instantiate_class(
                location=location,
                cls=cls,
                kwargs=kwargs,
            )

    def _check_and_instantiate_class(
        self,
        location: str,
        cls: Type[Any],
        args: Optional[Tuple[Any, ...]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> Any:
        class_location = join_class(location, get_class_name(cls))
        args = args or tuple()
        kwargs = kwargs or dict()

        if self._check_missings:
            check_missing_values(
                location=class_location,
                kwargs=kwargs,
                missing_value=self._missing_value,
            )

        if self._check_typings:
            check_params_type(
                cls=cls,
                args=args,
                kwargs=kwargs,
                location=class_location,
            )

        try:
            obj = cls(*args, **kwargs)
        except Exception as e:
            raise RuntimeError(f"Error during instantiate {class_location} class.") from e
        else:
            if isinstance(obj, Smart):
                obj.configurate(
                    keyword=self._keyword,
                    missing_value=self._missing_value,
                    location=location,
                    check_missings=self._check_missings,
                    check_typings=self._check_typings,
                    check_overrides=self._check_overrides,
                )

            return obj

    def _representation(self, obj: Any, skip_default: bool = False) -> Dict[str, Any]:
        representation: Dict[str, Any] = dict()
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
                        self._keyword: self.__class__.__name__,
                    }
                elif get_origin(annotation) is Smart or isinstance(default, Smart):
                    if isinstance(default, Smart):
                        param_type = default.type
                    else:
                        param_type, *_ = get_args(annotation)

                    keyword = inspect.formatannotation(param_type)
                    keyword = self._aliases.get(keyword, keyword)
                    keyword = join_class(keyword, get_class_name(self))

                    representation[name] = {
                        self._keyword: keyword,
                        **self._representation(param_type, skip_default),
                    }
                elif default is not inspect.Parameter.empty and skip_default:
                    continue
                elif default is None or isinstance(default, (bool, float, int, str)):
                    representation[name] = default
                elif annotation is not inspect.Parameter.empty and isinstance(annotation, type):
                    if annotation in (bool, float, int, str):
                        representation[name] = annotation.__name__ + self._missing_value
                    else:
                        keyword = inspect.formatannotation(annotation)
                        keyword = self._aliases.get(keyword, keyword)
                        representation[name] = {
                            self._keyword: keyword,
                            **self._representation(annotation, skip_default),
                        }
                else:
                    representation[name] = self._missing_value

        return representation

    def _register_classes(self, classes: Sequence[str]) -> None:
        self._register_aliases({item: item for item in classes})

    def _register_aliases(self, aliases: Mapping[str, str]) -> None:
        for origin, alias in aliases.items():
            if origin in self._aliases:
                raise ValueError(f"Origin '{origin}' has been overridden.")

            if alias in self._origins:
                raise ValueError(f"Alias '{alias}' has been overridden.")

            self._aliases[origin] = alias
            self._origins[alias] = origin
