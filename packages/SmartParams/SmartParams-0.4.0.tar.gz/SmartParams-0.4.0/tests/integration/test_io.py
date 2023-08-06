import tempfile
from pathlib import Path
from unittest.mock import Mock

from smartparams.io import load_data, print_data, save_data
from tests.unit import UnitCase


class TestLoadData(UnitCase):
    def test_load_data__yaml(self) -> None:
        expected = dict(key='value')
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir, 'config', 'params.yaml')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('key: value\n')

            actual = load_data(path=path)

            self.assertEqual(expected, actual)

    def test_load_data__yaml_not_dict(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir, 'config', 'params.yaml')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('value\n')

            self.assertRaises(ValueError, load_data, path=path)

    def test_load_data__not_exists(self) -> None:
        path = Path('config', 'params.exe')

        self.assertRaises(FileNotFoundError, load_data, path=path)

    def test_load_data__unknown(self) -> None:
        path = Mock(is_file=Mock(return_value=True), suffix='params.exe')

        self.assertRaises(ValueError, load_data, path=path)

    def test_load_data__no_extension(self) -> None:
        path = Mock(is_file=Mock(return_value=True), suffix='')

        self.assertRaises(ValueError, load_data, path=path)


class TestPrintData(UnitCase):
    def test_print_data__unknown(self) -> None:
        data = dict(key='value')
        fmt = 'exe'

        self.assertRaises(ValueError, print_data, data=data, fmt=fmt)


class TestSaveData(UnitCase):
    def test_save_data__yaml(self) -> None:
        data = dict(key='value')
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir, 'config', 'params.yaml')

            save_data(data=data, path=path)

            self.assertTrue(path.exists())
            self.assertEqual('key: value\n', path.read_text())

    def test_save_data__unknown(self) -> None:
        data = dict(key='value')
        path = Path('config', 'params.exe')

        self.assertRaises(ValueError, save_data, data=data, path=path)

    def test_save_data__no_extension(self) -> None:
        path = Mock(is_file=Mock(return_value=True), suffix='')

        self.assertRaises(ValueError, save_data, data=Mock(), path=path)
