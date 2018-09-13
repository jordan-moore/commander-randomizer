import requests
import json
import math
import time
from tqdm import tqdm
from random import randint


MAX_CARD_RESULTS = 175

all_commanders = list()
monocolored_commanders = list()
multicolored_commanders = list()
#cards = list()


class Card(object):
    name = ""
    scryfall_uri = 0
    png = ""
    color_identity = ""
    id = ""

    # The class "constructor" - It's actually an initializer
    def __init__(self, name, id, scryfall_uri, png, color_identity):
        self.name = name
        self.id = id
        self.scryfall_uri = scryfall_uri
        self.png = png
        self.color_identity = color_identity

    def __str__(self):
        return '{\'name\': \'' + str(self.name) + '\', \'id\': \'' + str(self.id) + '\', \'scryfall_uri\': \'' + str(self.scryfall_uri) + '\', \'png\': \'' + str(self.png) + '\', \'color_identity\': ' + str(self.color_identity) + '}'


def get_all_commanders():
    return all_commanders


def get_commanders(page):
    url = "https://api.scryfall.com/cards/search"

    querystring = {"q": "f:commander is:commander", "order": "artist", "page": str(page)}

    headers = {
        'Content-Type': "application/json"
    }

    return requests.request("GET", url, headers=headers, params=querystring)


def add_cards(new_card_array, cards, page, last_page):
    cards = list(cards)

    print('Loading Cards Page ' + str(page) + ' of ' + str(last_page))

    for card in tqdm(new_card_array):
        # name, id, scryfall_uri, png, color_identity
        name = card['name']
        card_id = card['id']
        scryfall_uri = card['scryfall_uri']
        try:
            png = card['image_uris']['png']
        except KeyError:
            png = "No PNG Image"

        color_identity = card['color_identity']

        new_card = Card(name, card_id, scryfall_uri, png, color_identity)
        time.sleep(0.01)
        # print('Adding Card: ' + str(new_card))
        # print()

        cards.append(new_card)

    return cards


def get_commander(commanders):
    rand = randint(0, commanders.__len__() - 1)
    return commanders[rand]


def initialize():
    page = 1
    last_page = 1
    has_more = True
    new_card_data = []
    cards = list()
    num_commanders = 0

    while has_more is True:
        response = get_commanders(page)

        data = json.loads(response.text)

        # print("Response Data:")
        # print(str(data))

        if page == 1:
            num_commanders = 0
            new_card_data = []

        for key, value in data.items():
            if key == 'total_cards' and page == 1:
                num_commanders = int(value)
                last_page = str(math.ceil(num_commanders / MAX_CARD_RESULTS))
                print('Commanders Found: ' + str(num_commanders) + '\n')
            if key == 'has_more':
                has_more = bool(value)
                time.sleep(0.02)
                # print('Has More: ' + str(has_more))
                time.sleep(0.02)
            if key == 'data':
                new_card_data = value
                # print('New Card Data: ' + str(new_card_data))

        print()
        cards = add_cards(new_card_data, cards, page, last_page)

        time.sleep(0.02)
        print('\nCommanders: ' + str(cards.__len__()) + ' out of ' + str(num_commanders))
        time.sleep(0.02)

        page += 1

    print('Loading Complete!')

    global all_commanders
    global multicolored_commanders
    global monocolored_commanders

    all_commanders = cards.copy()

    for commander_n in cards:

        if len(commander_n.color_identity) < 2:
            monocolored_commanders.append(commander_n)
        else:
            multicolored_commanders.append(commander_n)

    print ("\nAll Commanders:")
    for card in all_commanders:
        print(card)

    print ("\nMonocolored Commanders:\n")
    for card in monocolored_commanders:
        print(card)

    print ("\nMulticolored Commanders:\n")
    for card in multicolored_commanders:
        print(card)
