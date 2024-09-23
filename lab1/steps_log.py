from math import isqrt
from fastpower import pow_mod

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


# Пример использования
a = 5
y = 9
p = 23

result = baby_step_giant_step(a, y, p)
if result is not None:
    print(f"Дискретный логарифм {a}^x mod {p} = {y}\nx = {result}")
else:
    print("Дискретный логарифм не найден.")
