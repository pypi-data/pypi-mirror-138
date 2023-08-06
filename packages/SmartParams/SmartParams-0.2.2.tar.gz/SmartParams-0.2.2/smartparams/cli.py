import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class CLIArguments:
    path: Optional[Path]
    dump: bool
    save: bool
    params: list[str]


def parse_arguments(
    path: Optional[Path],
    dump: bool,
    save: bool,
) -> CLIArguments:
    return _parse_arguments(
        arguments=sys.argv[1:],
        path=path,
        dump=dump,
        save=save,
    )


def _parse_arguments(
    arguments: list[str],
    path: Optional[Path],
    dump: bool,
    save: bool,
) -> CLIArguments:
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=Path, default=path)
    parser.add_argument('--dump', default=dump, action='store_true')
    parser.add_argument('--save', default=save, action='store_true')
    parser.add_argument('--set', '-s', default=list(), action='append')
    args = parser.parse_args(arguments)

    if path and args.path and not args.path.is_absolute():
        args.path = path.parent.joinpath(args.path)

    return CLIArguments(
        path=args.path,
        dump=args.dump,
        save=args.save,
        params=args.set,
    )
