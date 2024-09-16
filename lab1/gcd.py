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


res = gcd_xy(28, 19)
print(res)
