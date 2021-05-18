##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 17, 2021
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

from typing import List, Union


###############################################################################
## REVERSE ENDIAN
###############################################################################
def reverse_endian(
    numbers_as_strings: Union[str, List[str]]
) -> Union[str, List[str]]:
    single_element: bool = type(numbers_as_strings) is not list
    if single_element:
        numbers_as_strings = [numbers_as_strings]  # type: ignore
    reversed: List[str] = []
    for s in numbers_as_strings:
        reversed.append(s[::-1])
    return reversed if not single_element else reversed[0]
