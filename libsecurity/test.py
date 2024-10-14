import math


with open("data/elgamal.encode.txt", "r") as file:
    key = file.read().split("!")

message_decode = ""
key.pop()

for item in key:
    print(item[0])
