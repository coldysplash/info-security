# Трёхэтапный протокол позволяющий организовать обмен секретными сообщениями по открытой линии связи
# для лиц, которые не имеют защищенных каналов и скретных ключей.
# В основном используется для шифрования числовых ключей.

import random
from extralib import generate_prime_number, gcd, pow_mod


def shamir_protocol():
    with open(f"data/shamir.txt", "r") as file:
        m = int(file.readline())
    p = generate_prime_number(20, 100)

    # секретные числа абонента А
    c1, d1 = generate_shamir_generate(p)

    # секретные числа абонента B
    c2, d2 = generate_shamir_generate(p)

    # m < p
    # передаем сообщение используя трехступенчатый протокол
    x = []
    x.append(pow_mod(m, c1, p))
    x.append(pow_mod(x[0], c2, p))
    x.append(pow_mod(x[1], d1, p))
    x.append(pow_mod(x[2], d2, p))

    return x


# генерируем параметры такие что: c*d mod (p - 1) = 1
def generate_shamir_generate(p: int):
    p_1 = p - 1
    c = random.randint(1, 19)
    while gcd(c, p_1) != 1:
        c += 1
    d = pow(c, -1, p_1)

    return c, d


def main():
    print(*shamir_protocol())


if __name__ == "__main__":
    main()
