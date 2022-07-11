# Problem 27:
#     Quadratic Primes
#
# Description:
#     Euler discovered the remarkable quadratic formula:
#         n^2 + n + 41
#
#     It turns out that the formula will produce 40 primes for the consecutive integer values 0 ≤ n ≤ 39.
#     However, when n = 40, 40^2 + 40 + 41 = 40*(40+1) + 41 is divisible by 41,
#       and certainly when n = 41, 41^2 + 41 + 41 is clearly divisible by 41.
#
#     The incredible formula n^2 - 79n + 1601 was discovered,
#       which produces 80 primes for the consecutive values 0 ≤ n ≤ 79.
#     The product of the coefficients, −79 and 1601, is −126479.
#
#     Considering quadratics of the form:
#         n^2 + an + b, where |a| < 1000 and |b| < 1000
#         where |n| is the modulus/absolute value of n
#         e.g. |11| = 11 and |-4| = 4
#
#     Find the product of the coefficients, a and b,
#       for the quadratic expression that produces the maximum number of primes for consecutive values of n,
#       starting with n = 0.

from math import floor, sqrt
from typing import Tuple

# Global variables to keep track of primes as they are found
PRIME_LIST = []
PRIME_SET = set()
HIGHEST_CHECKED = 1


def is_prime(x: int) -> bool:
    """
    Returns True iff `x` is prime.
    Keeps track of known primes up to highest `x` ever given to function, to avoid redundant calls.
    If a new `x` is out of range of numbers checked so far,
      figure out all results up to and including `x`, for future usage.

    Args:
        x (int): Integer

    Returns:
        (bool): True iff `x` is prime
    """
    global PRIME_LIST
    global PRIME_SET
    global HIGHEST_CHECKED

    if x < 2:
        # Negatives, 0, and 1 not considered prime
        return False
    else:
        if x > HIGHEST_CHECKED:
            # Not yet checked, so check all numbers until x (inclusive)
            for y in range(HIGHEST_CHECKED+1, x+1):
                include_y = True
                y_mid = floor(sqrt(y)) + 1
                i = 0
                while i < len(PRIME_LIST) and PRIME_LIST[i] < y_mid:
                    p = PRIME_LIST[i]
                    if y % p == 0:
                        include_y = False
                        break
                    i += 1
                if include_y:
                    PRIME_LIST.append(y)
                    PRIME_SET.add(y)
            HIGHEST_CHECKED = x
        return x in PRIME_SET


def get_x_max(a: int, b: int) -> int:
    """
    Returns maximum value `x_max`
      such that for given `a` and `b`,
      and all x where 0 ≤ x ≤ x_max,
      x^2 + a*x + b is prime.

    Args:
        a (int): Integer
        b (int): Integer

    Returns:
        (int): Highest value of `x` consecutively up from zero,
                 such that the quadratic formula produces all primes.

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(a) == int
    assert type(b) == int

    x = 0
    while True:
        val = x**2 + a*x + b
        if is_prime(val):
            x += 1
            continue
        else:
            x -= 1
            break
    return x


def main(n: int) -> Tuple[int, int, int]:
    """
    Returns tuple of `a`, `b`, `x_max`,
      such that the quadratic formula x^2 + a*x + b
      produces the largest number of consecutive primes
      for 0 ≤ x ≤ x_max and |a|, |b| < n.

    Args:
        n (int): Natural number

    Returns:
        (Tuple[int, int, int]):
            Tuple of `a`, `b`, and `x_max`, so that for |a|, |b| < `n`,
              x^2 + a*x + b produces the largest number of consecutive primes
              for 0 ≤ x ≤ x_max.

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(n) == int and n > 0

    # Notes:
    # (1) When x = 0, we have x^2 + a*x + b = 0^2 + a*0 + b = b.
    #     So b at least needs to be positive and prime.
    #
    # (2) When x = 1, we have x^2 + a*x + b = 1^2 + a*1 + b = a + b + 1.
    #     This needs to be at least 2, so that it is prime.
    #       => a + b + 1 ≥ 2
    #       => a + b ≥ 1
    #       => a ≥ 1 - b
    #     So `a` needs to fit this bound, for a given `b`.
    #
    # (3) Suppose we know that (x^2 + a*x + b) is prime, and we fix such x.
    #     Then the next potential consecutive prime is (x+1)^2 + a*(x+1) + b.
    #     The difference between the two is:
    #       = [(x+1)^2 + a*(x+1) + b] - [x^2 + a*x + b]
    #       = [(x+1)^2 + a*(x+1)] - [x^2 + a*x]
    #       = [(x+1)^2 + a] - [x^2]
    #       = [(x^2 + 2x + 1) + a] - [x^2]
    #       = [2x + 1 + a]
    #     Since we know that every prime greater than 2 is odd,
    #       then the difference between any of those latter odd primes is even.
    #     Thus we must have (2x + 1 + a) be even,
    #       and so `a` is odd.
    #     This further constrains the potential values of `a` to be checked.

    # Since note #1 tells us `b` must be a prime,
    #   initialize the list of primes within range of given `n`
    #   by calling the helper function
    _ = is_prime(n-1)

    # Loop through possible values of b (prime numbers)
    global PRIME_LIST
    a_max = b_max = x_max = -1
    i_b = 0
    while PRIME_LIST[i_b] < n:
        b = PRIME_LIST[i_b]
        a_lo = 1 - b             # Lower bound of `a`, from note #2
        a_lo += (a_lo % 2 == 0)  # `a` must be odd, from note #3
        for a in range(a_lo, n, 2):
            x = get_x_max(a, b)
            if x > x_max:
                a_max, b_max, x_max = a, b, x
        i_b += 1
    return a_max, b_max, x_max


if __name__ == '__main__':
    num = int(input('Enter a natural number: '))
    a_best, b_best, x_highest = main(num)
    print('Quadratic formula producing the most consecutive primes:')
    print('  n^2 + ({})*n + ({})'.format(a_best, b_best))
    print('  where 0 ≤ n ≤ {}'.format(x_highest))
    print('Values:')
    for ind in range(x_highest+1):
        print('  n = {:3d} -> {:10d}'.format(ind, ind**2 + a_best * ind + b_best))
    print('Product of coefficients:')
    print('  a × b = {} × {} = {}'.format(a_best, b_best, a_best * b_best))
