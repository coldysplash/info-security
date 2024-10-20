from extra_lib.extralib import gcd_xy, generate_prime_number, is_prime
import hashlib
import pickle
import random


def md5_hash(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.digest()


def gen_public_parametrs():
    p, b, q, a = 0, 0, 0, 0
    while True:
        q = generate_prime_number(1, 5000)
        b = random.randint(1, 10000)
        p = b * q + 1
        if is_prime(p):
            break

    a = random.randint(2, p)
    while True:
        a += 1
        if pow(a, q, p) == 1:
            break

    return p, q, a


def gost_sign(input_file, p, q, a):
    x = random.randint(1, q)
    y = pow(a, x, p)

    h = md5_hash(input_file)

    r = []
    s = []

    for i in range(0, 16):
        h_ = h[i]
        while True:
            k = random.randint(1, q)
            r_ = pow(a, k, p) % q
            if r_ == 0:
                continue
            s_ = (k * h_ + x * r_) % q
            if s_ > 0:
                break
        r.append(r_)
        s.append(s_)

    with open(f"{input_file}.gost_s", "wb") as file:
        pickle.dump(r, file)
        pickle.dump(s, file)

    return y


def gost_sign_check(input_file, sign_file, y, p, q, a):
    h = md5_hash(input_file)

    r = []
    s = []
    with open(f"{sign_file}", "rb") as file:
        r = pickle.load(file)
        s = pickle.load(file)

    for i in range(0, 16):
        if r[i] >= q or s[i] >= q:
            print("fail")
            return -1
        T = gcd_xy(h[i], q)  # fail
        if T[1] < 0:
            h_inv = q + T[1]
        else:
            h_inv = T[1]
        u1 = (s[i] * h_inv) % q
        u2 = (-r[i] * h_inv) % q
        if u2 < 0:
            u2 += q
        v = ((pow(a, u1, p) * pow(y, u2, p)) % p) % q
        if v != r[i]:
            return -1

    return 0


def main():

    input_file = "dsign_lib/data/image.jpg"

    p, q, a = gen_public_parametrs()
    # подписываем файл
    y = gost_sign(input_file, p, q, a)
    # проверяем файл на подлинность
    print(gost_sign_check(input_file, f"{input_file}.gost_s", y, p, q, a))


if __name__ == "__main__":
    main()
