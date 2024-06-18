"""
A module for various helper methods
"""
# --- IMPORTS --- #
import random
import string
from hashlib import sha256


# --- HELPERS --- #
def get_random_string(max_chars=64):
    """
    We return a random string with max chars
    """
    random_string = ""
    for x in range(max_chars):
        random_string += random.choice(string.ascii_letters)
    return random_string


def hash256(hash_string: str) -> str:
    return sha256(hash_string.encode()).hexdigest()


# --- MATH --- #

def legendre_symbol(r: int, p: int):
    """
    Returns (r | p) = {
        0 if r % p == 0
        1 if r % p != 0 and r is a quadratic residue mod p
        -1 if r % p != 0 and r is a quadratic non-residue mod p
    }
    We use Euler's criterion which states:
        (r | p) = r^((p-1)/1) (mod p)
    """
    if r % p == 0:
        return 0
    else:
        criterion = pow(r, (p - 1) // 2, p)
        return -1 if criterion == p - 1 else 1


def is_quadratic_residue(n: int, p: int) -> bool:
    """
    Returns True if (n|p) != -1. (We include 0 as quadratic residues.)
    """
    return True if legendre_symbol(n, p) != -1 else False


def tonelli_shanks(n: int, p: int):
    """
    If n is a quadratic residue mod p, then we return an integer r such that r^2 = n (mod p).
    """

    # Verify n is a quadratic residue
    if not is_quadratic_residue(n, p):
        return None

    # Trivial case
    if n % p == 0:
        return 0

    # p = 3 (mod 4) case
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)

    # --- GENERAL CASE --- #
    # 1) Divide p-1 into its even and odd components by p-1 = 2^s * q, where q is odd and s >=1
    q = p - 1
    s = 0
    while q % 2 == 0:
        s += 1
        q //= 2

    # 2) Find a quadratic non residue
    z = 2
    while is_quadratic_residue(z, p):
        z += 1

    # 3) Configure initial variables
    m = s
    c = pow(z, q, p)
    t = pow(n, q, p)
    r = pow(n, (q + 1) // 2, p)

    # 4) Repeat until t == 1
    while t != 1:

        # First find the least integer i such that t^(2^i) = 1 (mod p)
        i = 0
        factor = t
        while factor != 1:
            i += 1
            factor = (factor * factor) % p

        # Reassign variables
        exp = 2 ** (m - i - 1)
        b = pow(c, exp, p)
        m = i
        c = (b * b) % p
        t = (t * c) % p
        r = (r * b) % p

    return r
