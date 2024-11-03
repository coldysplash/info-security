import random
from modules.extralib import generate_prime_number, gcd


class Player:
    name = ""
    P = 0

    def __init__(self, name, p_key):
        self.name = name
        self.hand = []
        self.P = p_key
        self.key_c = random.randint(1, self.P - 1)
        while gcd(self.key_c, self.P - 1) != 1:
            self.key_c += 1
        self.key_d = pow(self.key_c, -1, self.P - 1)


def generate_deck(input_deck_file, p):
    deck = []
    with open(input_deck_file, "r") as file:
        for line in file:
            card = tuple(line.split())
            deck.append(card)
    random.shuffle(deck)

    q_cards = len(deck)
    encode_deck = {}

    # Генерируем уникальные рандомные числа
    rand_keys = random.sample(range(1, p - 1), q_cards)

    for i in range(q_cards):
        encode_deck[rand_keys[i]] = deck[i]

    return rand_keys, encode_deck, q_cards


def print_hand(cards):
    print(*cards[0], *cards[1])


def print_board(cards):
    print(f"\nCards on the board:")
    for card in cards:
        print(*card)


def mental_poker(Players_Names: list):
    if len(Players_Names) < 2:
        print("Error! Minimum number of players two.")
        return -1

    p = generate_prime_number(1000, 10000)
    Players = [Player(name=name, p_key=p) for name in Players_Names]

    deck_config = "/home/coldysplash/programming/info-security/M_Poker/modules/deck.txt"
    deck_keys, deck, q_cards = generate_deck(deck_config, p)

    # шифруем и перемешиваем колоду
    encode_deck = deck_keys
    for player in Players:
        encode_deck = [pow(card, player.key_c, p) for card in encode_deck]
        random.shuffle(encode_deck)

    # расшифровываем и узнаем карты каждого игрока
    for player in Players:
        for j in range(2):
            rand_card = random.randint(0, q_cards - 1)
            for player2 in Players:
                if player != player2:
                    encode_deck[rand_card] = pow(
                        encode_deck[rand_card], player2.key_d, p
                    )
            encode_deck[rand_card] = pow(encode_deck[rand_card], player.key_d, p)

            if encode_deck[rand_card] in deck_keys:
                player.hand.append(deck[encode_deck[rand_card]])
                q_cards -= 1
                deck.pop(encode_deck[rand_card])
                encode_deck.pop(rand_card)

    # выкладываем 5 карт на игровой стол
    game_board = []
    for i in range(5):
        rand_card = random.randint(0, q_cards - 1)
        for player in Players:
            encode_deck[rand_card] = pow(encode_deck[rand_card], player.key_d, p)
            if encode_deck[rand_card] in deck_keys:
                game_board.append(deck[encode_deck[rand_card]])
                q_cards -= 1
                deck.pop(encode_deck[rand_card])
                encode_deck.pop(rand_card)

    for pl in Players:
        print(f'Player "{pl.name}" - ', end="")
        print_hand(pl.hand)

    print_board(game_board)
