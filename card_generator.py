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


class Card(object):
    name = ""
    scryfall_uri = 0
    png = ""
    color_identity = ""
    id = ""
    type_line = ""

    # The class "constructor" - It's actually an initializer
    def __init__(self, name, id, scryfall_uri, png, color_identity, type_line):
        # print()
        # print('Name: ' + name)
        # print('Color Identity: ' + str(color_identity))
        color_identity = remove_duplicates(color_identity)
        # print('Clean Color Identity: ' + str(color_identity))

        type_line = type_line.replace('Enchantment ', '')

        self.name = name
        self.id = id
        self.scryfall_uri = scryfall_uri
        self.png = png
        self.color_identity = color_identity
        self.type_line = type_line
        self.description = str()

        if 'Legendary Planeswalker' in type_line:
            types = type_line.split()
            i = 0
            for type in types:
                # print(str(i) + ': ' + type)
                i += 1
            self.description = ' planeswalker that goes by ' + types[3]
        elif 'Legendary Creature' in type_line:
            types = type_line.split()
            i = 0
            for type in types:
                # print(str(i) + ': ' + type)
                i += 1

            creature_types = list()
            for x in range(3,len(types)):
                creature_types.append(types[x])
                # print(types[x])
            # print('Creature Types: ' + str(creature_types))

            if creature_types[0][0] == 'A' or creature_types[0][0] == 'E' or creature_types[0][0] == 'I' or creature_types[0][0] == 'O' or creature_types[0][0] == 'U':
                self.description = self.description + 'n'
            self.description = self.description + ' '

            if len(creature_types) == 1:
                self.description = self.description + creature_types[0]
            elif len(creature_types) == 2:
                if creature_types[1][0] == 'A' or creature_types[1][0] == 'E' or creature_types[1][0] == 'I' or creature_types[1][0] == 'O' or creature_types[1][0] == 'U':
                    self.description = self.description + creature_types[0] + ' and an ' + creature_types[1]
                else:
                    self.description = self.description + creature_types[0] + ' and a ' + creature_types[1]
            else:
                x = 0
                for creature_type in creature_types:
                    if x == 0:
                        self.description = self.description + str(creature_type) + ', '
                    elif x == (len(creature_types) - 1):
                        self.description = self.description + str(creature_type)
                    else:
                        self.description = self.description + str(creature_type) + ', '
                    x += 1
        self.description = self.description + ' that\'s '

        # Color Identity Descripting
        if len(color_identity) < 1:
            self.description = self.description + 'colorless.'
        elif len(color_identity) == 1:
            self.description = self.description + 'mono ' + translate_color(color_identity[0]) + '.'
        elif len(color_identity) == 2:
            self.description = self.description + translate_color(color_identity[0]) + ' and ' + translate_color(color_identity[1]) + '.'
        else:
            x = 0
            for color in color_identity:
                if x == 0:
                    self.description = self.description + str(translate_color(color_identity[x])) + ', '
                elif x == (len(color_identity) - 2):
                    self.description = self.description + str(translate_color(color_identity[x])) + ' and '
                elif x == (len(color_identity) - 1):
                    self.description = self.description + str(translate_color(color_identity[x]))
                else:
                    self.description = self.description + str(translate_color(color_identity[x])) + ', '
                x += 1
        # print ('Description: ' + self.description)

    def __str__(self):
        return '{\'name\': \'' + str(self.name) + '\', \'id\': \'' + str(self.id) + '\', \'scryfall_uri\': \'' + str(self.scryfall_uri) + '\', \'png\': \'' + str(self.png) + '\'type_line\': \'' + str(self.type_line) + '\', \'color_identity\': ' + str(self.color_identity) + '}'


def remove_duplicates(a_list):
    final_list = []
    for num in a_list:
        if num not in final_list:
            final_list.append(num)
    return final_list


def get_all_commanders():
    return all_commanders


def get_monocolored_commanders():
    return monocolored_commanders


def get_multicolored_commanders():
    return multicolored_commanders


def get_commanders(page):
    url = "https://api.scryfall.com/cards/search"

    querystring = {"q": "f:commander is:commander", "order": "artist", "page": str(page)}

    headers = {
        'Content-Type': "application/json"
    }

    return requests.request("GET", url, headers=headers, params=querystring)


def translate_color(letter):
    if letter == 'W':
        color = 'White'
    elif letter == 'U':
        color = 'Blue'
    elif letter == 'B':
        color = 'Black'
    elif letter == 'R':
        color = 'Red'
    else:
        color = 'Green'
    return color


def add_cards(new_card_array, cards, page, last_page):
    cards = list(cards)

    print('Loading Cards Page ' + str(page) + ' of ' + str(last_page))

    for card in tqdm(new_card_array):
        # name, id, scryfall_uri, png, color_identity
        name = card['name']
        card_id = card['id']
        scryfall_uri = card['scryfall_uri']
        type_line = card['type_line']
        try:
            png = card['image_uris']['png']
        except KeyError:
            png = "No PNG Image"

        color_identity = card['color_identity']

        new_card = Card(name, card_id, scryfall_uri, png, color_identity, type_line)
        # time.sleep(0.01)
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
                # print('Commanders Found: ' + str(num_commanders) + '\n')
            if key == 'has_more':
                has_more = bool(value)
                # time.sleep(0.02)
                # print('Has More: ' + str(has_more))
                # time.sleep(0.02)
            if key == 'data':
                new_card_data = value
                # print('New Card Data: ' + str(new_card_data))

        # print()
        cards = add_cards(new_card_data, cards, page, last_page)

        # time.sleep(0.02)
        # print('\nCommanders: ' + str(cards.__len__()) + ' out of ' + str(num_commanders))
        # time.sleep(0.02)

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
    '''
    print ("\nAll Commanders:")
    for card in all_commanders:
        print(card)

    print ("\nMonocolored Commanders:\n")
    for card in monocolored_commanders:
        print(card)

    print ("\nMulticolored Commanders:\n")
    for card in multicolored_commanders:
        print(card)
    '''
