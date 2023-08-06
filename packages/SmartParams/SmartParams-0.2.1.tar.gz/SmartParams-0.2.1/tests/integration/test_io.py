import tempfile
from pathlib import Path

from smartparams.io import load, to_string
from tests.unit import UnitCase


class TestToString(UnitCase):
    def test_to_string__yaml_list(self) -> None:
        lst = [None, True, {'1': 2, '3': 4}]

        string = to_string(lst, 'yaml')

        self.assertEqual("- null\n- true\n- '1': 2\n  '3': 4\n", string)

    def test_to_string_yaml_dict(self) -> None:
        dictionary = {'1': [True, False], 3: None}

        string = to_string(dictionary, 'yaml')

        self.assertEqual("'1':\n- true\n- false\n3: null\n", string)

    def test_to_string_yaml_error(self) -> None:
        self.assertRaises(ValueError, to_string, dict(), 'unknown')


class TestLoad(UnitCase):
    def test_load__yaml(self) -> None:
        expected = dict(key='value')
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir, 'config', 'params.yaml')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('key: value\n')

            actual = load(path=path)

            self.assertEqual(expected, actual)

    def test_load__yaml_not_dict(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir, 'config', 'params.yaml')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('value\n')

            self.assertRaises(ValueError, load, path=path)

    def test_load__unknown(self) -> None:
        path = Path('config', 'params.exe')

        self.assertRaises(ValueError, load, path=path)

    def test_load__no_extension(self) -> None:
        path = Path('config', 'params')

        self.assertRaises(ValueError, load, path=path)
