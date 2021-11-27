##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: November 26, 2021
##   | |    | | \ \    ---------------------------------
##   |_|    |_|  \_\   https://github.com/pedrorrivero
##

## Copyright 2021 Pedro Rivero
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
## http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

from copy import copy
from typing import Any, Callable, Optional, Tuple, Union, cast


###############################################################################
## VALIDATE NATURAL NUMBER
###############################################################################
def validate_natural(number: int, zero: bool = False) -> None:
    """
    Raises ValueError with custom message if `number` is not in the naturals.

    Parameters
    ----------
    number: int
        The object to validate.
    zero: bool, default: False
        Count zero as a natural.

    Raises
    ------
    TypeError
        If `number` is not int.
    ValueError
        If `number` is not a natural number.
    """
    validate_type(number, int)
    if number < 0 or not zero and number == 0:
        raise ValueError(
            f"Invalid value {number} <{'=' if not zero else ''} 0."
        )


###############################################################################
## VALIDATE TYPE
###############################################################################
def validate_type(
    obj: Any,
    typ: Union[type, Tuple[type, ...]],
    obj_name: Optional[str] = None,
) -> None:
    """
    Raises TypeError with custom deprecation message if `obj` and
    `typ` do not match.

    Parameters
    ----------
    obj: Any
        The object to validate.
    typ: Union[type, Tuple[type, ...]]
        The correct object type(s).
    obj_name: Optional[str] = None
        Optional object name to include in error message.

    Raises
    ------
    TypeError
        If `obj` does not match `typ`.
    """
    if not istype(obj, typ):
        MESSAGE = f"Invalid object type {type(obj)}"
        MESSAGE += (
            f" in `{obj_name}` assignment" if obj_name is not None else ""
        )
        MESSAGE += (
            f", expected {typ}."
            if isinstance(typ, type)
            else f", expected <type '{typ}'>."
            # else "."
        )
        raise TypeError(MESSAGE)


###############################################################################
## ISTYPE
###############################################################################
def istype(obj: Any, typ: Union[type, Tuple[type, ...], None]) -> bool:
    """
    Returns True if `obj` is of type `typ`, False otherwise.

    Parameters
    ----------
    obj: Any
        Object to check type.
    typ: Union[type, Tuple[type, ...], None]
        Target type(s).

    Returns
    -------
    out: bool
        True if `obj` is of type `typ`, False otherwise.
    """
    if typ is None:
        return isinstance(obj, type(None))
    elif isinstance(typ, tuple):
        for t in typ:
            if istype(obj, t):
                return True
        return False
    try:
        try:
            return isinstance(obj, typ)
        except TypeError:
            return istyping(obj, typ)
    except IndexError:
        raise TypeError(
            f"Tuple index mismatch, expected <{typ}> but received {obj}."
        )
    except Exception:
        raise NotImplementedError(f"Typecheck not supported for <{typ}>.")


def istyping(obj: Any, typ: Any) -> bool:
    """
    Returns True if `obj` is of typing `typ` (i.e. typing module),
    False otherwise.

    Parameters
    ----------
    obj: Any
        Object to check type.
    typ: Any
        Target type from typing module.

    Returns
    -------
    out: bool
        True if `obj` is of type `typ`, False otherwise.
    """
    if typ is Any:
        return True
    origin = typ.__origin__
    if origin is Union:
        return istype(obj, typ.__args__)
    elif not isinstance(obj, origin):
        return False
    elif origin is list:
        return all([istype(o, typ.__args__) for o in obj])
    elif origin is tuple:
        return all([istype(o, typ.__args__[i]) for i, o in enumerate(obj)])
    else:
        raise NotImplementedError


###############################################################################
## TYPECHECK DECORATOR
###############################################################################
def typecheck(func: Callable) -> Callable:
    """
    This function decorator enforces strong typing by checking type annotations
    for parameters and return values at runtime.

    Parameters
    ----------
    func: Callable
        The funciton in which to enforce typechecking.

    Returns
    -------
    out: Callable
        The input function decorated with typechecking logic.

    Examples
    --------
    >>> @typecheck
    >>> def add_or_subtract(a: int, b: int, minus: bool = False) -> int:
    >>>     return a-b if minus else a+b
    >>>
    >>> try: add_or_subtract(1, 1, minus=None)
    >>> except Exception as e: print(e)
    Invalid object type <class 'NoneType'> in `minus` assignment,
    expected <class 'bool'>.
    """

    def decorator(*args: Any, **kwargs: Any):
        arg_types: dict = get_arg_types(func, len(args))
        kwarg_types: dict = get_kwarg_types(func, len(args))
        return_type: type = get_return_type(func)
        for index, (name, typ) in enumerate(arg_types.items()):
            validate_type(args[index], typ, obj_name=name)
        for name, value in kwargs.items():
            validate_type(value, kwarg_types[name], obj_name=name)
        return_value: Any = func(*args, **kwargs)
        validate_type(return_value, return_type, obj_name="return")
        return return_value

    return decorator


###############################################################################
## GET TYPE ANNOTATIONS
###############################################################################
def get_arg_types(func: Callable, num_args: int) -> dict:
    """
    Returns the dict of type annotations corresponding to `args`.

    Parameters
    ----------
    func: Callable
        Function to get type annotations from.
    num_args: int
        The total number of `args`.

    Returns
    -------
    out: dict
        Types corresponding to `args`.

    Notes
    -----
    Requires Python ^3.7 to have ordered elements in dict. Before said version
    `popitem()` removed a random element instead of the last one.
    """
    arg_types: dict = copy(func.__annotations__)
    while len(arg_types) > num_args:
        arg_types.popitem()
    return arg_types


def get_kwarg_types(func: Callable, num_args: int) -> dict:
    """
    Returns the dict of type annotations corresponding to `kwargs`.

    Parameters
    ----------
    func: Callable
        Function to get type annotations from.
    num_args: int
        The total number of `args` (i.e. not the number of `kwargs`).

    Returns
    -------
    out: dict
        Types corresponding to `kwargs`.
    """
    arg_types = get_arg_types(func, num_args)
    kwarg_types: dict = copy(func.__annotations__)
    for key in arg_types.keys():
        kwarg_types.pop(key)
    kwarg_types.pop("return")
    return kwarg_types


def get_return_type(func: Callable) -> type:
    """
    Returns the return type annotation.

    Parameters
    ----------
    func: Callable
        Function to get type annotations from.

    Returns
    -------
    out: type
        Return type in annotations.
    """
    return cast(type, func.__annotations__["return"])
