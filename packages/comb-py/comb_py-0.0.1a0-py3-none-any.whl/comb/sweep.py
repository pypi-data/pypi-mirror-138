"""Utilities for running sweeps."""

import abc
import argparse
import collections
import itertools
from typing import List

import numpy as np

import comb.registry
import comb.util

__all__ = ["Args", "Sweep", "add_arguments", "parse_args"]

comb.registry.add_helper_functions(__name__)


class Args:
    """Command line arguments for starting a job within a sweep.

    Usage:
        >>> args = Args("foo", bar = "baz")
        >>> print(args)
        foo --bar baz
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def _items(self):
        def _len(k):
            return min(len(k), 2)

        for key in sorted(sorted(self.kwargs.keys()), key=_len):
            yield key, self.kwargs[key]

    def iterate_arguments(self):
        for k, v in self._items():
            if len(k) == 1:
                dash = "-"
            else:
                dash = "--"
                k = k.replace("_", "-")
            if isinstance(v, bool):
                if not v:
                    continue
                v = ""
            else:
                v = str(v)

            yield f"{dash}{k}"
            if len(v):
                yield str(v)

    def __str__(self):
        args = itertools.chain.from_iterable([self.args, self.iterate_arguments()])
        return " ".join(args)


class _BaseSweep:
    pass


class Sweep(_BaseSweep):
    """Abstract base class for defining parameter sweeps.

    Sweeps consist of a grid search defined by overriding the
    `get_fixed_args` method and a random search defined by
    overriding the `get_random_args` method.

    The `get_fixed_args` method should define a dictionary. The
    values can be arguments, lists or arguments, tuples of arguments,
    or a combination thereof.

    All lists must have the same length. First, all single arguments
    are extended to become lists of this length. Arguments at the same
    position within the lists are grouped together. In the second step,
    the argument list is expaned by replacing the tuples by the outer
    product of the arguments within the tuples.

    Sweeps are iterable.

    Usage:
        >>> class MySweep(Sweep):
        ...   @property
        ...   def script(self):
        ...     return "foo.bar"
        ...
        ...   def get_random_args(self):
        ...     return {x = np.random.uniform(0, 1)}
        ...
        ...   def get_fixed_args(self):
        ...     return {a : [1, (2,3)], b = 1, c = [1, 2]}
        ...
        >>> sweep = MySweep(num_random_samples = 1)
        >>> for args in sweep: print(args)
        foo.bar -a 1 -b 1 -c 1 -x 0.423
        foo.bar -a 2 -b 1 -c 2 -x 0.423
        foo.bar -a 3 -b 1 -c 2 -x 0.423
    """

    def __init__(self, num_random_samples: int = 10):
        super().__init__()
        self.num_random_samples = num_random_samples

    def _iter_fixed_args_grid(self):
        dict_ = self.get_fixed_args()
        keys = list(dict_.keys())
        vals = [dict_[key] for key in keys]
        vals = comb.util.zip_repeat(vals)
        for val in vals:
            val = [v if isinstance(v, tuple) else (v,) for v in val]
            for new_val in itertools.product(*val):
                yield dict(zip(keys, new_val))

    def __iter__(self):
        for _ in range(self.num_random_samples):
            random_args = self.get_random_args()
            for kwargs in self._iter_fixed_args_grid():
                kwargs.update(random_args)
                yield Args(self.script, **kwargs)
        """
        for kwargs in self._iter_fixed_args_grid():
           print(kwargs)
           kwargs.update(self.get_random_args()) 
           for _ in range(self.num_random_samples):
                #kwargs.update(self.get_random_args())
                yield Args(self.script, **kwargs)
        """

    @property
    @abc.abstractmethod
    def script(self) -> dict:
        raise NotImplementedError()

    def get_random_args(self) -> dict:
        """Sample random arguments for the sweep."""
        return {}

    def get_fixed_args(self) -> dict:
        """Return fixed arguments for the sweep."""
        return {}


class SweepCollection(_BaseSweep):
    def __init__(self, *sweeps):
        super().__init__()
        for sweep in sweeps:
            if not isinstance(sweep, _BaseSweep):
                raise TypeError(f"Got invalid type in sweep collection: {sweep}.")
        self._sweeps = sweeps

    def __iter__(self):
        for sweep in self._sweeps:
            for args in sweep:
                yield args


"""
def add_group(name: str, groups: List[str]):
    factory = _SweepFactory.get_instance()

    class _SweepCollection(SweepCollection):

        def __init__(self, *args, **kwargs):
            super().__init__(*[
                factory.get_sweep(sweep)(*args, **kwargs) for sweep in groups
            ])

    factory.register_sweep(name, _SweepCollection)
"""


def add_arguments(parser: argparse.ArgumentParser):
    if parser is None:
        parser = argparse.ArgumentParser(description="Configure sweeps")
    parser.add_argument(
        "sweep",
        choices=get_options(limit=None),
        help="The sweep to run. Register sweeps with the @sweep.register decorator.",
    )
    parser.add_argument(
        "-n",
        "--num-random-samples",
        default=1,
        type=int,
        metavar="N",
        help="Number of random arguments to draw.",
    )
    return parser
