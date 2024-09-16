import random
from fastpower import pow_mod
import math


# проверка на то что число является простым
def is_prime(p):
    if p <= 1:
        return False

    b = int(math.sqrt(p))

    for i in range(2, b + 1):
        if p % i == 0:
            return False

    return True


# генерация первообразного корня от простого числа
def primitive_root(p):
    if not is_prime(p):
        return None

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


def generate_public_parameters():
    while True:
        p = random.randint(1, 10000)
        g = primitive_root(p)
        if g != None:
            break

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

    return shared_key_a, shared_key_b, public_a, public_b


def main():
    # generate secret keys
    private_a = random.randint(1, 20)
    private_b = random.randint(1, 20)

    shared_key_a, shared_key_b, public_a, public_b = DH_key_exchange(
        private_a, private_b
    )

    print(
        f"Shared Key A = {shared_key_a}\nShared Key B = {shared_key_b}\nPublic Key A = {public_a}\nPublic Key B = {public_b}"
    )


if __name__ == "__main__":
    main()
