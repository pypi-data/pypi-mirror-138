from pathlib import Path
from unittest.mock import Mock, patch

from smartparams.cli import CLIArguments, _parse_arguments, parse_arguments
from tests.unit import UnitCase


class TestParseArguments(UnitCase):
    @patch('smartparams.cli.sys', Mock(argv=['script.py', 'arg1', 'arg2']))
    @patch('smartparams.cli._parse_arguments')
    def test_parse_arguments(self, _parse_arguments: Mock) -> None:
        parse_arguments(
            path=None,
            dump=True,
            save=True,
        )

        _parse_arguments.assert_called_once_with(
            arguments=['arg1', 'arg2'],
            path=None,
            dump=True,
            save=True,
        )

    def test_parse_arguments__without_cli(self) -> None:
        arguments: list[str] = []
        path = Path('/home/params.yaml')
        dump = True
        save = True
        expected = CLIArguments(
            path=Path('/home/params.yaml'),
            dump=True,
            save=True,
            params=[],
        )

        actual = _parse_arguments(
            arguments=arguments,
            path=path,
            dump=dump,
            save=save,
        )

        self.assertEqual(expected, actual)

    def test_parse_arguments__with_cli(self) -> None:
        arguments = [
            '--path',
            'cli_params.yaml',
            '--dump',
            '--save',
            '-s',
            'key1=value1',
            '--set',
            'key2=value2',
        ]
        path = Path('/home/params.yaml')
        dump = True
        save = True
        expected = CLIArguments(
            path=Path('/home/cli_params.yaml'),
            dump=True,
            save=True,
            params=['key1=value1', 'key2=value2'],
        )

        actual = _parse_arguments(
            arguments=arguments,
            path=path,
            dump=dump,
            save=save,
        )

        self.assertEqual(expected, actual)

    def test_parse_arguments__with_cli_absolute_path(self) -> None:
        arguments = [
            '--path',
            '/cli_params.yaml',
            '--dump',
            '--save',
            '-s',
            'key1=value1',
            '--set',
            'key2=value2',
        ]
        path = Path('/home/params.yaml')
        dump = True
        save = True
        expected = CLIArguments(
            path=Path('/cli_params.yaml'),
            dump=True,
            save=True,
            params=['key1=value1', 'key2=value2'],
        )

        actual = _parse_arguments(
            arguments=arguments,
            path=path,
            dump=dump,
            save=save,
        )

        self.assertEqual(expected, actual)
