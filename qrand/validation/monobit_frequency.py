from math import erfc, sqrt

from . import ValidationStrategy


class MonobitFrequencyValidation(ValidationStrategy):
    """
    Frequency tests the bitstring to ensure randomness

    Methods
    ----------
    validate(bitstring:str) -> bool
        validates the bitsting according to the Frequency test[monobit] defined in
        'A Statistical Test Suite for Random and Pseudorandom Number Generators for Cryptographic Applications' <https://csrc.nist.gov/publications/detail/sp/800-22/rev-1a/final>
        pg 24

    """

    def validate(self, bitstring: str) -> bool:
        """
        PARAMETERS
        ----------
        bitstring: str
        The bitstring to be tested for randomness

        RETURNS
        -------
        out: bool
        `True` if succeeds, `False` otherwise.

        """
        n = len(bitstring)
        s_n = 0.0
        for bit in bitstring:
            s_n += 2 * int(bit) - 1
        s_obs = s_n / sqrt(n)
        p_value = erfc(s_obs / sqrt(2))
        return p_value > 0.01
