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


# tests


# def test1():
#     a = 7
#     b = 5
#     m = 15
#     print(f"{a}**{b} % {m} = {pow_mod(a, b, m)}")


# def test2():
#     a = 2
#     b = 8
#     m = 10
#     print(f"{a}**{b} % {m} = {pow_mod(a, b, m)}")


# test1()
# test2()
