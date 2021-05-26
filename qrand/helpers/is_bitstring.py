##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 25, 2021
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

###############################################################################
## IS BITSTRING
###############################################################################
def is_bitstring(bitstring: str) -> bool:
    """
    Returns `True` if the input str is a bitstring, `False` otherwise.

    PARAMETERS
    ----------
    bitstring: str
        The string to check.

    RETURNS
    -------
    out: bool
        `True` if input str is bitstring, `False` otherwise.

    RAISES
    ------
    TypeError
        If input bitstring is not str.
    """
    if not isinstance(bitstring, str):
        raise TypeError(
            f"Invalid bitstring type '{type(bitstring)}'. Expected str."
        )
    b = {"0", "1"}
    s = set(bitstring)
    return s.issubset(b)
