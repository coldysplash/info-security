import math
import random


def pow_mod(a, b, m):
    result = 1
    a = a % m

    while b > 0:
        # Если b нечетное (остаток 1), умножаем результат на a
        if b % 2 == 1:
            result = result * a

        a = (a**2) % m
        b //= 2

    return result % m


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# ax + by = gcd(a, b)
def gcd_xy(a: int, b: int) -> list:
    T = [0, 0, 0]
    if a >= b:
        U = [a, 1, 0]
        V = [b, 0, 1]
    else:
        U = [a, 0, 1]
        V = [b, 1, 0]

    while T[0] != 1:
        q = U[0] // V[0]
        T[0] = U[0] % V[0]
        T[1] = U[1] - q * V[1]
        T[2] = U[2] - q * V[2]
        U = V
        V = T
    return T


# проверка на то что число является простым
def is_prime(p):
    if p <= 1:
        return False

    b = int(math.sqrt(p))

    for i in range(2, b + 1):
        if p % i == 0:
            return False

    return True


def generate_prime_number(a: int, b: int) -> int:
    while True:
        p = random.randint(a, b)
        if is_prime(p):
            return p


# генерация первообразного корня от простого числа
def primitive_root(p):

    phi = p - 1
    factors = []

    for i in range(2, int(phi**0.5) + 1):
        if phi % i == 0:
            factors.append(i)
            while phi % i == 0:
                phi //= i
    if phi > 1:
        factors.append(phi)

    for g in range(2, p):
        if all(pow(g, (p - 1) // fact, p) != 1 for fact in factors):
            return g

    return None
