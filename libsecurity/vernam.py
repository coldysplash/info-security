import random


def vernam_encode():
    with open(f"data/vernam.txt", "r") as file:
        messg = file.read()

    keys = []
    with open(f"data/vernam.encode.txt", "w") as file:
        for m in messg:
            k = random.randint(1, 300)
            e = ord(m) ^ k
            file.write(chr(e))
            keys.append(k)

    return keys


def vernam_decode(keys: list):

    with open(f"data/vernam.encode.txt", "r") as file:
        messg = file.read()

    messge_encode = ""
    i = 0
    while i < len(keys):
        messge_encode += chr(ord(messg[i]) ^ keys[i])
        i += 1

    return messge_encode


def main():
    keys = vernam_encode()
    decode_message = vernam_decode(keys)
    print(decode_message)


if __name__ == "__main__":
    main()
