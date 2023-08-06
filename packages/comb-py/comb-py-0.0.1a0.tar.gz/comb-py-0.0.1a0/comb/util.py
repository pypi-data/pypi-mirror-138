import itertools


def transpose_nested_lists(vals):
    """Transpose a list of lists.

    If a sublist does not contain a sufficient number of elements,
    missing elements will be filled with `None`.

    Usage:
        >>> l = [[11, 12] [21, 22] ]
        >>> print(transposed_nested_lists(l))
        [[11, 21] [12, 22]]

    Reference: https://stackoverflow.com/a/6473724
    """
    return list(map(list, itertools.zip_longest(*vals, fillvalue=None)))


def zip_repeat(vals):
    """Like itertools.zip_longest, but by repeating single elements."""

    lens = [len(val) for val in vals if isinstance(val, list)]
    num_runs = max(lens) if len(lens) > 0 else 1

    # Expand all lists to full length.
    vals = [
        (val if isinstance(val, list) else [val for _ in range(num_runs)])
        for val in vals
    ]
    # Transpose the list
    vals = transpose_nested_lists(vals)

    return vals
