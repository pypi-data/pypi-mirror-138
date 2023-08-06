from pathlib import Path
from unittest.mock import Mock, patch

from smartparams.cli import Arguments, parse_arguments
from tests.unit import UnitCase


class TestParseArguments(UnitCase):
    @patch('smartparams.cli.sys')
    def test_parse_arguments(self, sys: Mock) -> None:
        sys.argv = 'script.py'.split()
        expected = Arguments(
            path=Path('/home/params.yaml'),
            dump=False,
            skip_defaults=False,
            merge_params=False,
            print=None,
            format='yaml',
            params=[],
        )

        actual = parse_arguments(
            default_path=Path('/home/params.yaml'),
        )

        self.assertEqual(expected, actual)

    @patch('smartparams.cli.sys')
    def test_parse_arguments__override_path(self, sys: Mock) -> None:
        sys.argv = 'script.py --path /home/cli_params.yaml'.split()
        expected = Arguments(
            path=Path('/home/cli_params.yaml'),
            dump=False,
            skip_defaults=False,
            merge_params=False,
            print=None,
            format='yaml',
            params=[],
        )

        actual = parse_arguments(
            default_path=Path('/home/params.yaml'),
        )

        self.assertEqual(expected, actual)

    @patch('smartparams.cli.sys')
    def test_parse_arguments__dump(self, sys: Mock) -> None:
        sys.argv = 'script.py --dump -sm'.split()
        expected = Arguments(
            path=Path('/home/params.yaml'),
            dump=True,
            skip_defaults=True,
            merge_params=True,
            print=None,
            format='yaml',
            params=[],
        )

        actual = parse_arguments(
            default_path=Path('/home/params.yaml'),
        )

        self.assertEqual(expected, actual)

    @patch('smartparams.cli.sys')
    def test_parse_arguments__print_params(self, sys: Mock) -> None:
        sys.argv = 'script.py --print params --merge-params'.split()
        expected = Arguments(
            path=Path('/home/params.yaml'),
            dump=False,
            skip_defaults=False,
            merge_params=True,
            print='params',
            format='yaml',
            params=[],
        )

        actual = parse_arguments(
            default_path=Path('/home/params.yaml'),
        )

        self.assertEqual(expected, actual)

    @patch('smartparams.cli.sys')
    def test_parse_arguments__print_keys(self, sys: Mock) -> None:
        sys.argv = 'script.py --print keys --format yaml'.split()
        expected = Arguments(
            path=Path('/home/params.yaml'),
            dump=False,
            skip_defaults=False,
            merge_params=False,
            print='keys',
            format='yaml',
            params=[],
        )

        actual = parse_arguments(
            default_path=Path('/home/params.yaml'),
        )

        self.assertEqual(expected, actual)

    @patch('smartparams.cli.sys')
    def test_parse_arguments__required_path(self, sys: Mock) -> None:
        sys.argv = 'script.py'.split()

        with self.assertRaises(SystemExit) as context:
            parse_arguments()

        self.assertEqual(2, context.exception.code)

    @patch('smartparams.cli.sys')
    def test_parse_arguments__dump_print_error(self, sys: Mock) -> None:
        sys.argv = 'script.py --dump --print params'.split()

        self.assertRaises(SystemExit, parse_arguments, Path('/home/params.yaml'))

    @patch('smartparams.cli.sys')
    def test_parse_arguments__dump_format_error(self, sys: Mock) -> None:
        sys.argv = 'script.py --dump --format yaml'.split()

        self.assertRaises(SystemExit, parse_arguments, Path('/home/params.yaml'))

    @patch('smartparams.cli.sys')
    def test_parse_arguments__print_keys_skip_default_error(self, sys: Mock) -> None:
        sys.argv = 'script.py --print keys -s'.split()

        self.assertRaises(SystemExit, parse_arguments, Path('/home/params.yaml'))

    @patch('smartparams.cli.sys')
    def test_parse_arguments__print_keys_merge_params_error(self, sys: Mock) -> None:
        sys.argv = 'script.py --print keys -m'.split()

        self.assertRaises(SystemExit, parse_arguments, Path('/home/params.yaml'))
