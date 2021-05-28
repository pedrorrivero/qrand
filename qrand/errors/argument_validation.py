##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 28, 2021
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

from typing import Any, Optional
from warnings import warn


###############################################################################
## VALIDATE TYPE
###############################################################################
def validate_type(object: Any, type_class: type) -> None:
    """
    Raises TypeError with custom deprecation message if `object` and
    `type_class` do not match.

    Parameters
    ----------
    object: Any
        The object to validate.
    type_class: type
        The correct object type.

    Raises
    ------
    TypeError
        If `object` does not match `type_class`.
    """
    if not isinstance(object, type_class):
        raise TypeError(
            f"Invalid object type {type(object)}, \
            expected {type_class.__name__}."
        )


###############################################################################
## VALIDATE NATURAL NUMBER
###############################################################################
def validate_natural_number(number: int, zero: bool = False) -> None:
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
    MESSAGE = f"Invalid value {number} <{'=' if not zero else ''} 0."
    validate_type(number, int)
    if number < 0:
        raise ValueError(MESSAGE)
    elif not zero and number == 0:
        raise ValueError(MESSAGE)
