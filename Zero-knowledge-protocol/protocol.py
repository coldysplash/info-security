from extralib import generate_prime_number, gcd
import random


class Client:

    N = 0
    s = 0
    V = 0

    # получеам открытый параметр N от сервера
    # вычисляем секретный и открытый ключ клиента
    def __init__(self, name, N):
        self.name = name
        s = generate_prime_number(1, N - 1)
        while gcd(s, N) != 1:
            s += 1
        self.N = N
        self.s = s
        self.V = s**2 % N

    def get_public_key(self):
        return self.V

    def get_name(self):
        return self.name

    def generate_x(self):
        self.r = random.randint(1, self.N - 1)
        return self.r**2 % self.N

    def generate_y(self, e):
        return (self.r * self.s**e) % self.N


class Server:

    N = 0
    users = {}

    # добавляем в словарь users информацию о уже существующих пользователях
    def __init__(self):
        with open("users.txt", "r") as file:
            for line in file:
                info = line.split(",")
                self.users[info[0]] = info[1]

    def generate_pub_params(self):
        P = generate_prime_number(10000, 10000000)
        Q = generate_prime_number(10000, 10000000)
        self.N = P * Q
        return self.N

    def save_user(self, name, V):
        with open("users.txt", "a") as file:
            file.write(name + "," + str(V) + "\n")

    def generate_e(self):
        return random.randint(0, 1)

    # функция где клиент доказывает серверу, что он знает секретный ключ
    def verify_user(self, client: Client):

        V = client.get_public_key()

        # t - кол-во раундов(аккредитаций)
        t = 3
        for _ in range(t):
            # этап 1 - клиент вычисляет x и передает серверу
            x = client.generate_x()
            # этап 2 - сервер генерирует e(0, 1) и передает клиенту
            e = self.generate_e()
            # этап 3 - клиент вычисляет y и передает серверу
            y = client.generate_y(e)

            # проверяем что клиент знает s (секретный ключ)
            if (y**2 % self.N) == (x * V**e % self.N):
                continue
            else:
                return -1

        self.save_user(client.get_name(), V)
        return 0


def main():
    serv = Server()
    login_user = str(input("Введите свой логин > "))
    user = Client(login_user, serv.generate_pub_params())

    if login_user in serv.users:
        print("Пользователь с таким именем уже существует!")
        return -1

    if serv.verify_user(user) == 0:
        print("Пользователь успешно зарегестрирован!")
    else:
        print("Проверка не пройдена.")
        return -1

    return 0


if __name__ == "__main__":
    main()
