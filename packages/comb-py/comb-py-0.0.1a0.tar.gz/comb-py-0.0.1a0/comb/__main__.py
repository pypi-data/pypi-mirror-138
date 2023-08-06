"""Write parameter sweeps to stdout or files.

Place your sweep definitions in sweep and use the @register
decorator to add them to the list of options to select.
"""

import argparse
import importlib
import os
import sys

import comb.sweep

class Logger:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def info(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs, file=sys.stderr)

    def error(self, *args, **kwargs):
        print(*args, **kwargs, file=sys.stderr)
        sys.exit(1)

_logger = Logger()

def _iter_files(*searchpaths: str) -> bool:
    """Iterate over all files in the given searchpath."""
    for searchpath in searchpaths:
        if not os.path.exists(searchpath):
            _logger.error(
                f"You provided a search path or a file "
                f"which does not exist: {searchpath}"
            )
        if os.path.isdir(searchpath):
            for root, _, filenames in os.walk(searchpath):
                for filename in filenames:
                    yield os.path.join(root, filename)
        elif os.path.isfile(searchpath):
            yield searchpath
        else:
            raise ValueError(
                f"Undefined error when attempting to interpret "
                f"'{searchpath}' as a path."
            )


def _import_by_filename(filename: str):
    """Import python module by filename.

    Reference:
        CC BY SA 4.0, Sebastian Rittau, https://stackoverflow.com/a/67692
    """
    module_name = filename.split(".py", 1)[0]
    module_spec = importlib.util.spec_from_file_location(module_name, filename)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)


def _is_valid_sweep_module(filename: str) -> bool:
    """Check if the given filename is a valid python module.

    Valid python modules contain keywords indicating that
    a sweep is defined, and are regular python files ending in
    .py.
    """
    if not filename.endswith(".py"):
        return False
    if filename.startswith("_"):
        return False
    with open(filename, "r") as fh:
        search = "register", "Sweep"
        content = fh.read()
        matches = sum(int(s in content) for s in search)
        if matches < 2:
            return False
    return True


def _import_modules(*searchpaths):
    """Import all python modules containing sweeps from the given paths."""
    for filename in filter(_is_valid_sweep_module, _iter_files(*searchpaths)):
        _import_by_filename(filename)


def _parse_arguments(parser: argparse.ArgumentParser) -> argparse.Namespace:
    parser.add_argument(
        "-i",
        "--searchpath",
        default=["sweep"],
        nargs="+",
        help="Search directory to look for sweep files, or path to single file.",
    )
    args, remaining_kwargs = parser.parse_known_args()
    _import_modules(*args.searchpath)

    parser = comb.sweep.add_arguments(parser=parser)
    parser.add_argument(
        "-w",
        "--write",
        action="store_true",
        help="Write arguments to file in the sweep directory.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output file to write to. Implies -w.",
    )
    parser.add_argument("-d", "--dir", help="Directory for writing sweep files.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print log messages to stderr.")
    return parser.parse_args(remaining_kwargs)


def cli():
    parser = argparse.ArgumentParser(description="Configure sweeps")
    args = _parse_arguments(parser)
    _logger.verbose = args.verbose

    sweep = comb.sweep.init(args.sweep, num_random_samples=args.num_random_samples)
    job_id = 0
    if args.output is not None:
        setattr(args, "write", True)

    if args.write:
        if args.output is None:
            if args.dir is None or not os.path.exists(args.dir):
                _logger.error(
                    f"Provide a valid output directory. You provided {args.dir}."
                )
            setattr(args, "output", os.path.join(args.dir, args.sweep + ".lst"))
        _logger.info(f"Writing to {args.output}.")
        file_ = open(args.output, "w")
    else:
        file_ = sys.stdout

    try:
        for job_id, cmd in enumerate(sweep):
            print(cmd, file=file_)
            if file_ != sys.stdout:
                _logger.info(job_id, cmd)
    except Exception as e:
        _logger.info(f"{type(e).__name__} occured: {e}")
    finally:
        if args.write:
            file_.close()
            _logger.info(f"Wrote {1+job_id} jobs to {args.output}.")


if __name__ == "__main__":
    cli()
