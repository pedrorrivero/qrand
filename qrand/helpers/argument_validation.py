##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: November 25, 2021
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

from typing import Any, Tuple, Union


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
    object: Any, classinfo: Union[type, Tuple[type, ...]]
) -> None:
    """
    Raises TypeError with custom deprecation message if `object` and
    `classinfo` do not match.

    Parameters
    ----------
    object: Any
        The object to validate.
    classinfo: Union[type, Tuple[type, ...]]
        The correct object type(s).

    Raises
    ------
    TypeError
        If `object` does not match `classinfo`.
    """
    MESSAGE = f"Invalid object type {type(object)}"
    MESSAGE += (
        f", expected {classinfo.__name__}."
        if isinstance(classinfo, type)
        else "."
    )
    if not isinstance(object, classinfo):
        raise TypeError(MESSAGE)
