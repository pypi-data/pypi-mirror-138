import inspect
from typing import Any
from unittest.mock import Mock

from smartparams import Smart
from smartparams.utils import get_hints, get_name, get_nested
from tests.custom_classes import Class, ClassCompositionChild
from tests.unit import UnitCase


class TestGetNested(UnitCase):
    def setUp(self) -> None:
        self.dict = dict(arg1='arg1', arg2=['arg2'], arg3={'arg31': 'a31', 'arg32': 'a32'})

    def test_nested(self) -> None:
        name = 'arg3.arg31'

        dictionary, key = get_nested(dictionary=self.dict, name=name)

        self.assertEqual('arg31', key)
        self.assertTupleEqual((('arg31', 'a31'), ('arg32', 'a32')), tuple(dictionary.items()))

    def test_nested__not_in_dictionary(self) -> None:
        name = 'missing.any'

        self.assertRaises(KeyError, get_nested, dictionary=self.dict, name=name)

    def test_nested__ensure_key_exists(self) -> None:
        name = 'arg3.missing'

        self.assertRaises(
            KeyError,
            get_nested,
            dictionary=self.dict,
            name=name,
            ensure_key_exists=True,
        )

    def test_nested__not_is_dictionary(self) -> None:
        name = 'arg3.arg31.a31'

        self.assertRaises(ValueError, get_nested, dictionary=self.dict, name=name)

    def test_nested__create_missing_directories(self) -> None:
        name = 'arg3.missing.key'

        dictionary, key = get_nested(
            dictionary=self.dict,
            name=name,
            create_missing_directories=True,
        )

        self.assertIsInstance(dictionary, dict)
        self.assertFalse(bool(dictionary))
        self.assertEqual('key', key)


class TestGetName(UnitCase):
    def test_get_name(self) -> None:
        test_cases = (
            (Mock, 'Mock'),
            (Mock(), 'Mock'),
            (123, 'int'),
            (type, 'type'),
            (None, 'NoneType'),
            (lambda: ..., '<lambda>'),
            ((i for i in range(1)), '<genexpr>'),
        )

        for cls, expected in test_cases:
            with self.subTest(expected=expected):
                actual = get_name(cls)  # type: ignore

                self.assertEqual(expected, actual)


class TestGetHints(UnitCase):
    def test_get_name(self) -> None:
        test_cases = (
            (
                ClassCompositionChild,
                {
                    'cls': Class,
                    'smart_cls': Smart[Class],
                    'smart': Smart,
                    'unknown': Any,
                    'no_type': Any,
                    'args': tuple[Any, ...],
                    'smart_cls_with_default': Smart[Class],
                    'smart_cls_with_only_default_generic': Smart,
                    'with_only_default_primitive': int,
                    'kwargs': dict[str, Any],
                },
            ),
        )

        for cls, expected in test_cases:
            signature = inspect.signature(cls)

            with self.subTest(cls=cls.__name__):
                actual = get_hints(signature)

                self.assertEqual(expected, actual)
