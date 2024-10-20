# Позволяет передавать сообщения не имея защищенного канала используя одну пересылку

from extra_lib.extralib import generate_prime_number, primitive_root


def elgamal_generate(p, g):
    # секретное число
    c = generate_prime_number(1, p - 1)
    # открытое число
    d = pow(g, c, p)

    return c, d


def elgamal_encode(p, g, d):
    with open(f"encryption_lib/data/elgamal.txt", "r") as file:
        messg = file.read()

    with open(f"encryption_lib/data/elgamal.encode.txt", "w") as file:
        for ch in messg:
            k = generate_prime_number(1, p - 2)
            r = pow(g, k, p)
            e = ord(ch) * d**k % p

            file.write(chr(r))
            file.write(chr(e))


def elgamal_decode(p, c):
    with open("encryption_lib/data/elgamal.encode.txt", "r") as file:
        messg = file.read()

    message_decode = ""
    messg = list(messg)

    for i in range(0, len(messg), 2):
        r = ord(messg[i])
        e = ord(messg[i + 1])
        m = (e * r ** (p - 1 - c)) % p
        message_decode += chr(m)

    return message_decode


def main():
    p = generate_prime_number(1000, 5000)
    g = primitive_root(p)
    # генерируем параметры для абонентов
    A = list(elgamal_generate(p, g))
    B = list(elgamal_generate(p, g))
    # Абонент А шифрует, Абонент B расшифровывает
    # (B[1] - открытый ключ d_b, B[0] - закрытый ключ c_a)

    elgamal_encode(p, g, B[1])

    decode_mesg = elgamal_decode(p, B[0])

    print(f"{decode_mesg}")


if __name__ == "__main__":
    main()
