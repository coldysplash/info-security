import random
from extralib import generate_prime_number, gcd


def rsa_generate():
    P = generate_prime_number(1, 1000)
    Q = generate_prime_number(1, 1000)
    N = P * Q

    f = (P - 1) * (Q - 1)
    d = random.randint(1, f - 1)
    while gcd(d, f) != 1:
        d += 1
    c = pow(d, -1, f)

    return c, d, N


def rsa_encode(d, N):
    with open(f"encryption_lib/data/rsa.txt", "r") as file:
        messg = file.read()

    with open(f"encryption_lib/data/rsa.encode.txt", "w") as file:
        for m in messg:
            e = pow(ord(m), d, N)

            file.write(chr(e))


def rsa_decode(c, N):
    with open("encryption_lib/data/rsa.encode.txt", "r") as file:
        messg = file.read()

    message_decode = ""
    for e in messg:
        m = pow(ord(e), c, N)
        message_decode += chr(m)

    return message_decode


def main():
    A = list(rsa_generate())
    B = list(rsa_generate())

    rsa_encode(d=B[1], N=B[2])
    decode_mesg = rsa_decode(c=B[0], N=B[2])

    print(f'"{decode_mesg}" - decode message from A')


if __name__ == "__main__":
    main()
