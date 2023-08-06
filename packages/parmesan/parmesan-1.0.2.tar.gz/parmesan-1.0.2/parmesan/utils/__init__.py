# system modules
import sys
import itertools
import inspect
import warnings

# internal modules
import parmesan.utils.string
import parmesan.utils.mode
import parmesan.utils.function

# external modules


def find_object(x):
    """
    Generator yielding tuples of module and variable name pointing to a given
    object.

    Args:
        x (object): the object to look for

    Yields:
        module_name, variable_name : the location of the variable
    """
    for module_name, module in sys.modules.copy().items():
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore", category=(DeprecationWarning, FutureWarning)
                )
                for name, var in inspect.getmembers(module):
                    if var is x:
                        yield module_name, name
        except BaseException:
            continue


def doc(x, s):
    """
    Set the docstring of a given object and return it
    """
    x.__doc__ = s
    return x


def is_iterable(x):
    """
    Check if a given object is iterable but not a string.
    """
    if isinstance(x, str):
        return False
    try:
        iter(x)
    except TypeError:
        return False
    return True


def single_argument_combinations(d):
    """
    Given a dict mapping argument names to (sequences of) possible values,
    return an iterable of all single argument combinations yielding :any:`dict`
    s with only one argument as key and the next value.

    For example:

    .. code-block:: python

        single_argument_combinations({"a":[1,2,3],"b":[4,5,6]})
        # yields sequentially
        {'a': 1}
        {'a': 2}
        {'a': 3}
        {'b': 4}
        {'b': 5}
        {'b': 6}
    """
    return (
        dict((t,))
        for t in itertools.chain.from_iterable(
            itertools.product((k,), v if is_iterable(v) else (v,))
            for k, v in d.items()
        )
    )


def all_argument_combinations(d):
    """
    Given a dict mapping argument names to (sequences of) possible values,
    return an iterable of all argument combinations yielding :any:`dict` s of
    the same size as the input but only one value.

    For example:

    .. code-block:: python

        all_argument_combinations({"a":[1,2,3],"b":[4,5,6]})
        # yields sequentially
        {'a': 1, 'b': 4}
        {'a': 1, 'b': 5}
        {'a': 1, 'b': 6}
        {'a': 2, 'b': 4}
        {'a': 2, 'b': 5}
        {'a': 2, 'b': 6}
        {'a': 3, 'b': 4}
        {'a': 3, 'b': 5}
        {'a': 3, 'b': 6}
    """
    return map(
        dict,
        itertools.product(
            *(
                (
                    itertools.product(
                        (arg,), values if is_iterable(values) else (values,)
                    )
                )
                for arg, values in d.items()
            )
        ),
    )
