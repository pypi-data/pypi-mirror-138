from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union
from unittest.mock import Mock, patch

from smartparams.smart import Smart
from tests.custom_classes import Class
from tests.unit import UnitCase


class TestSmartInitCase(UnitCase):
    def setUp(self) -> None:
        self.smart = Smart(Class, arg1='arg1', arg2=10)

    def test_params(self) -> None:
        params = self.smart.params

        self.assertEqual(dict(arg1='arg1', arg2=10), params)
        self.assertIsNot(self.smart._params, params)

    def test_call(self) -> None:
        obj = self.smart()

        self.assertIsInstance(obj, Class)
        self.assertEqual('arg1', obj.arg1)
        self.assertEqual(10, obj.arg2)

    def test_call__with_params(self) -> None:
        smart = Smart(Class)

        obj = smart('a1', arg2=15)

        self.assertIsInstance(obj, Class)
        self.assertEqual('a1', obj.arg1)
        self.assertEqual(15, obj.arg2)

    def test_call__with_duplicated_params(self) -> None:
        smart = Smart(Class, arg1='arg1')

        self.assertRaises(TypeError, smart, 'a1')

    def test_call__without_class(self) -> None:
        smart: Smart = Smart()

        self.assertRaises(AttributeError, smart)


class TestSmartAccessCase(UnitCase):
    def setUp(self) -> None:
        self.smart: Smart = Smart(arg1='arg1', arg2=['arg2'], arg3={'arg31': 'a31', 'arg32': 'a32'})

    def test_keys(self) -> None:
        keys = self.smart.keys()

        self.assertTupleEqual(('arg1', 'arg2', 'arg3'), tuple(keys))

    def test_get(self) -> None:
        value = self.smart.get('arg3.arg31')

        self.assertEqual('a31', value)

    def test_set(self) -> None:
        new_value = 'argument31'

        value = self.smart.set('arg3.arg31', new_value)

        self.assertEqual('argument31', value)
        self.assertEqual('argument31', self.smart.params['arg3']['arg31'])
        self.assertEqual('a32', self.smart.params['arg3']['arg32'])

    def test_pop(self) -> None:
        value = self.smart.pop('arg3.arg31')

        self.assertEqual('a31', value)
        self.assertFalse('arg3' in self.smart.params['arg3'])

    def test_map(self) -> None:
        function = Mock(return_value='argument31')

        value = self.smart.map('arg3.arg31', function)

        self.assertEqual('argument31', value)
        self.assertEqual('argument31', self.smart.params['arg3']['arg31'])
        self.assertEqual('a32', self.smart.params['arg3']['arg32'])

    @patch('smartparams.smart.load_data')
    def test_update(self, load_data: Mock) -> None:
        dictionary = {'arg1': {'nested1': 'argument1'}, 'arg3': {'arg31': 'argument31'}}
        load_data.return_value = dictionary
        test_cases: List[Tuple[Union['Smart', Dict[str, Any], List[str], Path], str]] = [
            (Smart(**dictionary), "smart"),
            (dictionary, "dict"),
            (['arg3.arg31=argument31', 'arg1={"nested1": "argument1"}'], "list"),
            (Path('path/to/file.yaml'), "path"),
        ]

        for source, msg in test_cases:
            smart: Smart = deepcopy(self.smart)

            with self.subTest(msg=msg):
                smart.update(source)

                self.assertTrue('arg1' in smart.params)
                self.assertTrue('arg2' in smart.params)
                self.assertTrue('arg3' in smart.params)
                self.assertEqual({'nested1': 'argument1'}, smart.params['arg1'])
                self.assertListEqual(['arg2'], smart.params['arg2'])
                self.assertEqual('argument31', smart.params['arg3']['arg31'])
                self.assertEqual('a32', smart.params['arg3']['arg32'])

    @patch('smartparams.smart.load_data')
    def test_update__not_override(self, load_data: Mock) -> None:
        dictionary = {'arg1': {'nested1': 'aa1'}, 'arg3': {'arg31': 'aa31'}, 'arg4': {'a4': 'aa4'}}
        load_data.return_value = dictionary
        test_cases: List[Tuple[Union['Smart', Dict[str, Any], List[str], Path], str]] = [
            (Smart(**dictionary), "smart"),
            (dictionary, "dict"),
            (['arg3.arg31=argument31', 'arg1={"nested1": "aa1"}', 'arg4={"a4": "aa4"}'], "list"),
            (Path('path/to/file.yaml'), "path"),
        ]

        for source, msg in test_cases:
            smart: Smart = deepcopy(self.smart)

            with self.subTest(msg=msg):
                smart.update(source, override=False)

                self.assertTrue('arg1' in smart.params)
                self.assertTrue('arg2' in smart.params)
                self.assertTrue('arg3' in smart.params)
                self.assertEqual('arg1', smart.params['arg1'])
                self.assertListEqual(['arg2'], smart.params['arg2'])
                self.assertEqual('a31', smart.params['arg3']['arg31'])
                self.assertEqual('a32', smart.params['arg3']['arg32'])
                self.assertEqual({'a4': 'aa4'}, smart.params['arg4'])

    def test_update__with_name(self) -> None:
        dictionary = {'arg': {'nested': ['arg3.arg31=argument31', 'arg1={"nested1": "argument1"}']}}

        self.smart.update(dictionary, name='arg.nested')

        self.assertTrue('arg1' in self.smart.params)
        self.assertTrue('arg2' in self.smart.params)
        self.assertTrue('arg3' in self.smart.params)
        self.assertEqual({'nested1': 'argument1'}, self.smart.params['arg1'])
        self.assertListEqual(['arg2'], self.smart.params['arg2'])
        self.assertEqual('argument31', self.smart.params['arg3']['arg31'])
        self.assertEqual('a32', self.smart.params['arg3']['arg32'])

    def test_update__with_name_error(self) -> None:
        dictionary = {'arg': {'nested': ['arg3.arg31 argument31']}}

        self.assertRaises(RuntimeError, self.smart.update, dictionary, name='arg.nested')

    def test_update__unknown(self) -> None:
        source = tuple()  # type: ignore

        self.assertRaises(TypeError, self.smart.update, source)

    def test_flatten_keys(self) -> None:
        value = self.smart.flatten_keys()

        self.assertListEqual(['arg1', 'arg2', 'arg3.arg31', 'arg3.arg32'], value)


class TestSmartInstantiateCase(UnitCase):
    def setUp(self) -> None:
        self.class_name = f"{Class.__module__}.{Class.__qualname__}"
        self.params = dict(
            smart_dict={'class': 'Smart'},
            smart={'class': self.class_name + ':Smart', 'arg1': 'arg1', 'arg2': 10},
            object={'class': self.class_name, 'arg1': 'arg1', 'arg2': 10},
            value=21,
        )
        self.smart: Smart = Smart(**self.params)

    def test_get__init_smart(self) -> None:
        obj = self.smart.get('smart', init=True)

        self.assertIsInstance(obj, Smart)
        self.assertIs(obj.type, Class)
        self.assertTrue('smart' in self.smart.params)

    def test_get__init_object(self) -> None:
        obj = self.smart.get('object', init=True)

        self.assertIsInstance(obj, Class)
        self.assertTrue('object' in self.smart.params)

    def test_get__init_value(self) -> None:
        obj = self.smart.get('value', init=True)

        self.assertIsInstance(obj, int)
        self.assertTrue('value' in self.smart.params)

    def test_get__init_persist(self) -> None:
        obj = self.smart.get('object', init=True, persist=True)

        self.assertIs(self.smart.get('object', init=True, persist=False), obj)
        self.assertIsInstance(self.smart.get('object'), Class)
        self.assertTrue('object' in self.smart.params)

    def test_get__init_not_persist(self) -> None:
        obj = self.smart.get('object', persist=False)

        self.assertIsNot(self.smart.get('object', init=True, persist=False), obj)
        self.assertIsInstance(self.smart.get('object'), dict)
        self.assertTrue('object' in self.smart.params)

    def test_pop__init_smart(self) -> None:
        obj = self.smart.pop('smart', init=True)

        self.assertIsInstance(obj, Smart)
        self.assertIs(obj.type, Class)
        self.assertFalse('smart' in self.smart.params)

    def test_pop__init_object(self) -> None:
        obj = self.smart.pop('object', init=True)

        self.assertIsInstance(obj, Class)
        self.assertFalse('object' in self.smart.params)

    def test_pop__init_value(self) -> None:
        obj = self.smart.pop('value', init=True)

        self.assertIsInstance(obj, int)
        self.assertFalse('value' in self.smart.params)

    def test_instantiate__any(self) -> None:
        data = "string"

        result = self.smart._instantiate(data, '')

        self.assertEqual(data, result)

    def test_instantiate__smart_dict(self) -> None:
        obj = self.params['smart_dict']

        result = self.smart._instantiate(obj, '')

        self.assertIsInstance(result, Smart)
        self.assertIsNone(result.type)

    def test_instantiate__smart(self) -> None:
        obj = self.params['smart']

        result = self.smart._instantiate(obj, '')

        self.assertIsInstance(result, Smart)
        self.assertIs(result.type, Class)

    def test_instantiate__unknown(self) -> None:
        obj = self.params['smart']
        obj['class'] += "suffix"  # type: ignore

        self.assertRaises(ValueError, self.smart._instantiate, obj, '')

    def test_instantiate__object(self) -> None:
        obj = self.params['object']

        result = self.smart._instantiate(obj, '')

        self.assertIsInstance(result, Class)

    def test_instantiate__dict(self) -> None:
        obj = {'key': 'value'}

        result = self.smart._instantiate(obj, '')

        self.assertIsNot(obj, result)

    def test_instantiate__list(self) -> None:
        obj = ['item']

        result = self.smart._instantiate(obj, '')

        self.assertIsNot(obj, result)

    def test_instantiate___with_aliases(self) -> None:
        self.smart._allow_only_registered = True
        self.smart._aliases = {self.class_name: 'Class'}
        self.smart._origins = {v: k for k, v in self.smart._aliases.items()}
        obj = self.params['object']
        obj['class'] = 'Class'  # type: ignore

        result = self.smart._instantiate(obj, '')

        self.assertIsInstance(result, Class)

    def test_instantiate___with_aliases_not_used(self) -> None:
        self.smart._aliases = {self.class_name: 'Class'}
        self.smart._origins = {v: k for k, v in self.smart._aliases.items()}
        obj = self.params['object']

        result = self.smart._instantiate(obj, '')

        self.assertIsInstance(result, Class)

    def test_instantiate___with_aliases_error(self) -> None:
        self.smart._allow_only_registered = True
        self.smart._aliases = {self.class_name: 'Class'}
        self.smart._origins = {v: k for k, v in self.smart._aliases.items()}
        obj = self.params['object']

        self.assertRaises(ImportError, self.smart._instantiate, obj, '')


class TestRegisterCase(UnitCase):
    def setUp(self) -> None:
        self.smart: Smart = Smart()

    def test_register__classes(self) -> None:
        classes = ('origin.1', 'origin.2')

        self.smart.register(classes)

        self.assertFalse(self.smart._allow_only_registered)
        self.assertEqual({'origin.1': 'origin.1', 'origin.2': 'origin.2'}, self.smart._aliases)
        self.assertEqual({'origin.1': 'origin.1', 'origin.2': 'origin.2'}, self.smart._origins)

    def test_register__aliases(self) -> None:
        aliases = {'origin.1': 'alias.1', 'origin.2': 'alias.2'}

        self.smart.register(aliases)

        self.assertFalse(self.smart._allow_only_registered)
        self.assertEqual({'origin.1': 'alias.1', 'origin.2': 'alias.2'}, self.smart._aliases)
        self.assertEqual({'alias.1': 'origin.1', 'alias.2': 'origin.2'}, self.smart._origins)

    def test_register__alias_duplicates(self) -> None:
        self.smart._aliases = {'origin': 'alias'}
        self.smart._origins = {'alias': 'origin'}
        aliases = {'origin.1': 'alias'}

        self.assertRaises(ValueError, self.smart.register, aliases)

    def test_register__origin_duplicates(self) -> None:
        self.smart._aliases = {'origin': 'alias'}
        self.smart._origins = {'alias': 'origin'}
        aliases = {'origin': 'alias.1'}

        self.assertRaises(ValueError, self.smart.register, aliases)

    def test_register__raise(self) -> None:
        self.assertRaises(TypeError, self.smart.register, Mock())

    def test_register__nested(self) -> None:
        self.smart._location = 'nested'

        self.assertRaises(AttributeError, self.smart.register, Mock())


class TestConfigurationCase(UnitCase):
    def setUp(self) -> None:
        self.smart: Smart = Smart()

    def test_configurate__allow_only_registered_true(self) -> None:
        self.smart.configurate(
            allow_only_registered=True,
        )

        self.assertTrue(self.smart._allow_only_registered)

    def test_configurate__allow_only_registered_false(self) -> None:
        self.smart.configurate(
            allow_only_registered=False,
        )

        self.assertFalse(self.smart._allow_only_registered)

    def test_configurate__allow_only_registered_false_raise(self) -> None:
        self.smart._allow_only_registered = True

        self.assertRaises(AttributeError, self.smart.configurate, allow_only_registered=False)
