from encryption_lib.rsa import rsa_generate
import hashlib
import pickle


def md5_hash(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.digest()


def rsa_sign(input_file: str, c, N):
    y = md5_hash(input_file)

    s = []
    for i in range(0, 16):
        s.append(pow(y[i], c, N))

    with open(f"{input_file}.rsa_s", "wb") as file:
        pickle.dump(s, file)


def rsa_sign_check(input_file, sign_file, d, N):

    s = []
    with open(f"{sign_file}", "rb") as file:
        s = pickle.load(file)

    h = md5_hash(input_file)
    for i in range(0, 16):
        w = pow(s[i], d, N)
        if h[i] != w:
            return -1

    return 0


def main():
    input_file = "dsign_lib/data/image.jpg"
    c, d, N = rsa_generate()

    # подписываем файл
    rsa_sign(input_file, c, N)

    # проверяем файл на подлинность
    res_sign = rsa_sign_check(input_file, f"{input_file}.rsa_s", d, N)
    if res_sign != 0:
        print("Подпись не является подлинной!")
    else:
        print("Подпись подлинная!")


if __name__ == "__main__":
    main()
