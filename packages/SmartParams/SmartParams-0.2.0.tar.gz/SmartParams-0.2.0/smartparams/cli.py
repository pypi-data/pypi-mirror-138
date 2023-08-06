import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class CLIArguments:
    path: Optional[Path]
    dump: bool
    keys: bool
    print_format: str
    params: list[str]


def parse_arguments(
    path: Optional[Path],
    dump: bool,
    keys: bool,
    print_format: str,
) -> CLIArguments:
    return _parse_arguments(
        arguments=sys.argv[1:],
        path=path,
        dump=dump,
        keys=keys,
        print_format=print_format,
    )


def _parse_arguments(
    arguments: list[str],
    path: Optional[Path],
    dump: bool,
    keys: bool,
    print_format: str,
) -> CLIArguments:
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=Path, default=path)
    parser.add_argument('--dump', default=dump, action='store_true')
    parser.add_argument('--keys', default=keys, action='store_true')
    parser.add_argument('--print_format', type=str, default=print_format)
    parser.add_argument('--set', '-s', default=list(), action='append')
    args = parser.parse_args(arguments)

    if path and args.path and not args.path.is_absolute():
        args.path = path.parent.joinpath(args.path)

    return CLIArguments(
        path=args.path,
        dump=args.dump,
        keys=args.keys,
        print_format=args.print_format,
        params=args.set,
    )
