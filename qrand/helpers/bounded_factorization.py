##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 20, 2021
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

from .argument_validation import validate_natural


###############################################################################
## COMPUTE BOUNDED FACTORIZATION
###############################################################################
def compute_bounded_factorization(
    n: int, bound_A: int, bound_B: int
) -> Tuple[int, int]:
    """
    f: ℕ³ → D ⊆ ℕ² such that f(n, A, B) = (a, b) minimizes n-a•b, where:
        1. a•b ≤ n < A•B
        2. a ≤ A < n and b ≤ B < n
        3. f(a•b, A, B) = (a', b') : a•b = a'•b'

    Parameters
    ----------
    n: int
        The natural number to factor.
    bound_A: int
        The bound for the first factor a.
    bound_B: int
        The bound for the second factor b.

    Notes
    -----
    Notice how we require A < n otherwise the trivial solution (a=n, b=1) would
    be available. The same applies to B < n. Additionally, we require n < A•B
    to scape the trivial solution (a=A, b=B).

    The last (stability) condition is needed to guarantee performance (i.e.
    running the algorithm iteratively does not worsen the approximation).
    Notice that this condition is automatically satisfied if the function
    always returns an optimal solution. However, since (a, b) ∈ D —as opposed
    to being general natural numbers— this condition is, in principle, less
    restrictive than asking for perfect factoring of any given composite
    number.

    By convention, we assume zero to not be contained in the natural numbers
    (ℕ).

    Although we do not provide a formal proof, we believe this problem to be
    beyond NP. This is so because it reduces to the factoring problem for
    A = B = n-1, when n is the product of only two primes. Additionally,
    verifying an answer does not seem to be efficient either, since we do not
    know a way of finding the optimal gap n-a•b without going through the same
    process required for solving the problem to begin with.

    The algorithm currently used finds the optimal solution through exhaustive
    search.
    """
    _validate_args(n, bound_A, bound_B)
    if bound_A * bound_B < n:
        return bound_A, bound_B
    swapped: bool = bound_A > bound_B
    bound_A, bound_B = sorted([bound_A, bound_B])
    final_delta: int = n
    b: int = bound_B
    a: int = n // b
    delta: int = n - a * b
    while a <= bound_A and a <= b and final_delta != 0:
        if delta < final_delta:
            final_a, final_b, final_delta = a, b, delta
        a += 1
        b = n // a
        delta = n - a * b
    return (final_b, final_a) if swapped else (final_a, final_b)


def _validate_args(n: int, bound_A: int, bound_B: int) -> None:
    validate_natural(n, zero=False)
    validate_natural(bound_A, zero=False)
    validate_natural(bound_B, zero=False)
