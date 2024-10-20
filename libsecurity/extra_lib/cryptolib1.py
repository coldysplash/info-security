import random
from extralib import *
import math
from math import isqrt


def generate_public_parameters():
    p = generate_prime_number(10, 1000)
    g = primitive_root(p)
    return p, g


def DH_key_exchange(private_a: int, private_b: int):
    # generate public parameters
    prime, g_root = generate_public_parameters()

    # generate public key for Alice
    public_a = pow_mod(g_root, private_a, prime)

    # generate public key for Bob
    public_b = pow_mod(g_root, private_b, prime)

    # generate shared private key
    shared_key_a = pow_mod(public_b, private_a, prime)
    shared_key_b = pow_mod(public_a, private_b, prime)

    return shared_key_a, shared_key_b


# a**x % p = y  x = ??  p > y mk > p
def baby_step_giant_step(a, y, p):
    # Выбор параметров m и k
    m = isqrt(p) + 1
    k = isqrt(p) + 1

    # Первый ряд: Шаги младенца (baby steps)
    baby_steps = {pow_mod(a, j, p): j for j in range(m)}

    # Второй ряд: Шаги великана (giant steps)
    # Находим a^(-m) mod p - обратный элемент по модулю
    a_inv_m = pow_mod(a, p - 1 - m, p)

    current = y
    for i in range(k):
        if current in baby_steps:
            return i * m + baby_steps[current]
        current = (current * a_inv_m) % p

    return None


def testDH():
    # generate secret keys
    private_a = random.randint(1, 20)
    private_b = random.randint(1, 20)

    shared_key_a, shared_key_b = DH_key_exchange(private_a, private_b)

    print(f"Shared Key A = {shared_key_a}\nShared Key B = {shared_key_b}")


def test_bg_steps():
    a = 5
    y = 9
    p = 23

    result = baby_step_giant_step(a, y, p)
    if result is not None:
        print(f"Дискретный логарифм {a}^x mod {p} = {y}\nx = {result}")
    else:
        print("Дискретный логарифм не найден.")


def main():
    testDH()
    # test_bg_steps()


if __name__ == "__main__":
    main()
