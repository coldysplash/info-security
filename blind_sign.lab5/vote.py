from extralib import generate_prime_number, gcd
from rsa import rsa_generate
import random
import hashlib


class Server:
    c = 0
    d = 0
    N = 0

    def __init__(self):
        self.c, self.d, self.N = rsa_generate()

    def get_public_params(self):
        return self.d, self.N

    def sign_vote(self, h_encr):
        return pow(h_encr, self.c, self.N)

    def check_sign(self, sign, h_encry):
        if sign != h_encry:
            return -1
        else:
            return 0


def client(res_vote: str, server: Server):
    d, N = server.get_public_params()
    rnd = random.randint(100, 10000)
    v = 0
    for ch in res_vote:
        v += ord(ch)
    n = rnd + v
    r = generate_prime_number(1, N - 1)
    while gcd(r, N) != 1:
        r += 1

    hash_n = hashlib.sha256(str(n).encode()).digest()

    h_encryption = 0
    for i in range(16):
        h_encryption += (hash_n[i] * r**d) % N

    s_encry = server.sign_vote(h_encryption)

    r_inv = pow(r, -1, N)
    sign = (s_encry * r_inv) % N

    return server.check_sign(sign, h_encryption)


if __name__ == "__main__":
    server = Server()
    d, N = server.get_public_params()
    if client("Yes", server) == 0:
        print("The signature is genuine!")
    else:
        print("Wrong note sign!")
