import pickle as pkl
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from smartparams import Smart
from tests.custom_classes import (
    Class,
    ClassChild,
    ClassComposition,
    RaiseClass,
    some_function,
)
from tests.unit import UnitCase


class TestSerialization(UnitCase):
    def setUp(self) -> None:
        class_name = f"{Class.__module__}.{Class.__qualname__}"
        class_child_name = f"{ClassChild.__module__}.{ClassChild.__qualname__}"
        self.smart = Smart(
            ClassComposition,
            **{
                'cls': {'arg1': 'argument1', 'arg2': 15, 'class': class_name},
                'smart': {'class': 'Smart'},
                'smart_cls': {'arg1': 'str???', 'arg2': 75, 'class': f'{class_name}:Smart'},
                'unknown': some_function,
                'smart_cls_with_default': {
                    'arg1': 'argument1',
                    'arg2': 5,
                    'class': f'{class_child_name}:Smart',
                },
            },
        )

    def test_pickle(self) -> None:
        pickled = pkl.dumps(self.smart)
        smart = pkl.loads(pickled)

        self.assertIsInstance(smart, Smart)
        self.assertEqual(str(self.smart), str(smart))
        self.assertIs(smart.type, ClassComposition)
        self.assertEqual(self.smart.params, smart.params)


class TestSmartRunCase(UnitCase):
    def setUp(self) -> None:
        self.smart = Smart(Class, arg2=10)

    @patch('smartparams.cli.sys', Mock(argv=[]))
    def test_run__dump_save_with_path(self) -> None:
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.yaml') as file:
            self.smart.run(path=Path(file.name), dump=True, save=True)

            self.assertEqual("arg1: str???\narg2: 10\n", file.read())

    @patch('smartparams.cli.sys', Mock(argv=[]))
    @patch('smartparams.smart.print')
    def test_run__dump_without_path(self, print_mock: Mock) -> None:
        self.smart.run(path=None, dump=True)

        print_mock.assert_called_once_with("arg1: str???\narg2: 10\n---\n- arg1\n- arg2\n")

    @patch('smartparams.cli.sys', Mock(argv=[]))
    @patch('smartparams.smart.print')
    def test_run__dump_save_without_path(self, print_mock: Mock) -> None:
        self.smart.run(path=None, dump=True, save=True)

        print_mock.assert_called_with("Cannot save if path is not specified.", file=sys.stderr)

    @patch('smartparams.smart.load', Mock(return_value={'arg1': 'string'}))
    def test_run__function(self) -> None:
        function = Mock()
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.yaml') as file:
            file.write("arg1: string\n")
            file.seek(0)

            self.smart.run(function=function, path=Path(file.name))

            function.assert_called_once_with(self.smart)

    @patch('smartparams.smart.load', Mock(return_value={'arg1': 'string'}))
    def test_run__self(self) -> None:
        self.smart._class = Mock()  # type: ignore
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.yaml') as file:
            file.write("arg1: string\n")
            file.seek(0)

            self.smart.run(path=Path(file.name))

            self.smart._class.assert_called_once_with(arg1='string', arg2=10)  # type: ignore


class TestSmartRepresentationCase(UnitCase):
    def setUp(self) -> None:
        self.smart: Smart = Smart()

    def test_representation__with_defaults(self) -> None:
        class_name = f"{Class.__module__}.{Class.__qualname__}"
        class_child_name = f"{ClassChild.__module__}.{ClassChild.__qualname__}"
        expected = {
            'cls': {'class': class_name, 'arg1': 'str???', 'arg2': 5},
            'smart_cls': {'class': f'{class_name}:Smart', 'arg1': 'str???', 'arg2': 5},
            'smart': {'class': 'Smart'},
            'unknown': '???',
            'smart_cls_with_default': {
                'class': f'{class_child_name}:Smart',
                'arg1': 'str???',
                'arg2': 5,
            },
            'smart_cls_with_only_default_generic': {
                'class': 'Smart',
            },
        }

        actual = self.smart._representation(ClassComposition, skip_default=False)

        self.assertEqual(expected, actual)

    def test_representation__without_defaults(self) -> None:
        class_name = f"{Class.__module__}.{Class.__qualname__}"
        class_child_name = f"{ClassChild.__module__}.{ClassChild.__qualname__}"
        expected = {
            'cls': {'class': class_name, 'arg1': 'str???'},
            'smart_cls': {'class': f'{class_name}:Smart', 'arg1': 'str???'},
            'smart': {'class': 'Smart'},
            'unknown': '???',
            'smart_cls_with_default': {
                'class': f'{class_child_name}:Smart',
                'arg1': 'str???',
            },
            'smart_cls_with_only_default_generic': {
                'class': 'Smart',
            },
        }

        actual = self.smart._representation(ClassComposition, skip_default=True)

        self.assertEqual(expected, actual)

    def test_representation__with_aliases(self) -> None:
        class_name = f"{Class.__module__}.{Class.__qualname__}"
        class_child_name = f"{ClassChild.__module__}.{ClassChild.__qualname__}"
        self.smart._allow_only_registered = True
        self.smart._aliases = {class_name: 'Parent', class_child_name: 'Child'}
        self.smart._origins = {v: k for k, v in self.smart._aliases.items()}
        expected = {
            'cls': {'class': 'Parent', 'arg1': 'str???', 'arg2': 5},
            'smart_cls': {'class': 'Parent:Smart', 'arg1': 'str???', 'arg2': 5},
            'smart': {'class': 'Smart'},
            'unknown': '???',
            'smart_cls_with_default': {
                'class': 'Child:Smart',
                'arg1': 'str???',
                'arg2': 5,
            },
            'smart_cls_with_only_default_generic': {
                'class': 'Smart',
            },
        }

        actual = self.smart._representation(ClassComposition, skip_default=False)

        self.assertEqual(expected, actual)


class TestCheckCase(UnitCase):
    def setUp(self) -> None:
        self.smart = Smart(Class, arg1='str???', arg2=15)

    @patch('smartparams.smart.warnings')
    def test_check_and_init_class__check_false(self, warnings: Mock) -> None:
        self.smart.check_missings = False
        self.smart.check_overrides = False
        self.smart.check_typings = False

        obj = self.smart(arg2='88')

        self.assertIsInstance(obj, Class)
        self.assertEqual('88', obj.arg2)
        warnings.warn.assert_not_called()

    @patch('smartparams.smart.warnings')
    def test_check_and_init_class__check_missings_true(self, warnings: Mock) -> None:
        self.smart.check_missings = True
        self.smart.check_overrides = False
        self.smart.check_typings = False

        self.assertRaises(ValueError, self.smart, arg2='88')
        warnings.warn.assert_not_called()

    @patch('smartparams.smart.warnings')
    def test_check_and_init_class__check_missings_none(self, warnings: Mock) -> None:
        self.smart.check_missings = None
        self.smart.check_overrides = False
        self.smart.check_typings = False

        obj = self.smart(arg2='88')

        self.assertIsInstance(obj, Class)
        self.assertEqual('88', obj.arg2)
        warnings.warn.assert_called()

    @patch('smartparams.smart.warnings')
    def test_check_and_init_class__check_overrides_true(self, warnings: Mock) -> None:
        self.smart.check_missings = False
        self.smart.check_overrides = True
        self.smart.check_typings = False

        self.assertRaises(ValueError, self.smart, arg2='88')
        warnings.warn.assert_not_called()

    @patch('smartparams.smart.warnings')
    def test_check_and_init_class__check_overrides_none(self, warnings: Mock) -> None:
        self.smart.check_missings = False
        self.smart.check_overrides = None
        self.smart.check_typings = False

        obj = self.smart(arg2='88')

        self.assertIsInstance(obj, Class)
        self.assertEqual('88', obj.arg2)
        warnings.warn.assert_called()

    @patch('smartparams.smart.warnings')
    def test_check_and_init_class__check_typings_true(self, warnings: Mock) -> None:
        self.smart.check_missings = False
        self.smart.check_overrides = False
        self.smart.check_typings = True

        self.assertRaises(TypeError, self.smart, arg2='88')
        warnings.warn.assert_not_called()

    @patch('smartparams.smart.warnings')
    def test_check_and_init_class__check_typings_none(self, warnings: Mock) -> None:
        self.smart.check_missings = False
        self.smart.check_overrides = False
        self.smart.check_typings = None

        obj = self.smart(arg2='88')

        self.assertIsInstance(obj, Class)
        self.assertEqual('88', obj.arg2)
        warnings.warn.assert_called()

    def test_check_and_init_class__location(self) -> None:
        smart = Smart(Smart, nested=[{'class': 'Smart'}])
        smart._location = 'location'

        obj = smart()

        self.assertIsInstance(obj, Smart)
        self.assertEqual('location.nested.0', obj.get('nested')[0]._location)

    def test_check_and_init_class__raise(self) -> None:
        smart = Smart(RaiseClass)

        self.assertRaises(Exception, smart)
