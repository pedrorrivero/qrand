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

from typing import Tuple


###############################################################################
## COMPUTE BOUNDED FACTORIZATION
###############################################################################
def compute_bounded_factorization(
    n: int, bound_A: int, bound_B: int
) -> Tuple[int, int]:
    if bound_A * bound_B < n:
        return bound_A, bound_B
    swapped: bool = bound_A > bound_B
    bound_A, bound_B = sorted([bound_A, bound_B])
    final_b: int = bound_B
    final_a: int = n // final_b
    final_delta: int = n - final_a * final_b
    a: int = final_a + 1
    b: int = n // a
    delta: int = n - a * b
    while a <= bound_A and a <= b and final_delta != 0:
        if delta < final_delta:
            final_a, final_b, final_delta = a, b, delta
        a += 1
        b = n // a
        delta = n - a * b
    return (final_b, final_a) if swapped else (final_a, final_b)
