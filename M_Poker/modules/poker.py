import random
from modules.extralib import generate_prime_number, gcd


class Player:
    name = ""
    P = 0

    def __init__(self, name, p_key):
        self.name = name
        self.u = []
        self.v = []
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


def mental_poker(Players_Names: list):
    if len(Players_Names) < 2:
        print("Error! Minimum number of players two.")
        return -1

    p = generate_prime_number(100, 10000)
    Players = [Player(name=name, p_key=p) for name in Players_Names]

    deck_config = "/home/coldysplash/programming/info-security/M_Poker/modules/deck.txt"
    deck_keys, deck, q_cards = generate_deck(deck_config, p)

    for player in Players:
        player.u = [pow(card, player.key_c, p) for card in deck_keys]
        random.shuffle(player.u)
        for j in range(0, 2):
            rand_card = random.randint(0, q_cards - 1)
            for player2 in Players:
                if player == player2:
                    card_key = pow(player.u[rand_card], player.key_d, p)
                else:
                    player2.v = [pow(card, player2.key_c) for card in player.u]
                    w = pow(player2.v[rand_card], player.key_d, p)
                    card_key = pow(w, player2.key_d, p)

                if card_key in deck_keys:
                    player.hand.append(deck[card_key])
                    q_cards -= 1
                    deck_keys.remove(card_key)
                    deck.pop(card_key)

    for pl in Players:
        print(f"{pl.name}, {pl.hand}\n")
