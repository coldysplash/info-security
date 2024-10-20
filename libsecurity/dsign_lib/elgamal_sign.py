from encryption_lib.elgamal import elgamal_generate
from extra_lib.extralib import generate_prime_number, gcd, primitive_root
import hashlib
import pickle


def md5_hash(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.digest()


def elgamal_sign(input_file: str, x, p, g):
    h = md5_hash(input_file)

    k = generate_prime_number(1, p - 1)
    while gcd(k, p - 1) != 1:
        k += 1

    r = pow(g, k, p)

    k_inv = pow(k, -1, p - 1)

    s = []
    for i in range(0, 16):
        if h[i] >= p:
            return -1
        u = (h[i] - x * r) % (p - 1)
        s.append(k_inv * u % (p - 1))

    with open(f"{input_file}.elgml_s", "wb") as file:
        pickle.dump(r, file)
        pickle.dump(s, file)

    return 0


def elgamal_sign_check(input_file, sign_file, p, g, y):

    r = 0
    s = []
    with open(f"{sign_file}", "rb") as file:
        r = pickle.load(file)
        s = pickle.load(file)

    h = md5_hash(input_file)
    for i in range(0, 16):
        left = pow(y, r, p) * pow(r, s[i], p) % p
        right = pow(g, h[i], p)
        if left != right:
            return -1

    return 0


def main():

    input_file = "dsign_lib/data/image.jpg"
    p = generate_prime_number(1000, 5000)
    g = primitive_root(p)
    x, y = elgamal_generate(p, g)

    # подписываем файл
    if elgamal_sign(input_file, x, p, g) == -1:
        print("Ошибка при создании подписи!")
    else:
        print("Файл успешно подписан!")

    # проверяем файл на подлинность
    elgml_sign_res = elgamal_sign_check(input_file, f"{input_file}.elgml_s", p, g, y)
    if elgml_sign_res != 0:
        print("Подпись не является подлинной!")
    else:
        print("Подпись подлинная!")


if __name__ == "__main__":
    main()
