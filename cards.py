import os
from dotenv import load_dotenv

from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity

load_dotenv()
API_KEY = os.getenv('API_KEY')

from pokemontcgsdk import RestClient
RestClient.configure(API_KEY)








def get_sets():
    global all_sets

    sets = Set.all()
    all_sets = []
    for set in sets:
        raw_set = str(set).replace('Set', '').replace('=', '').replace('(', '').replace(')', '').replace("'",'').split(',')
        if(raw_set[5] == ' standardLegal'):
            format = 'standard'
        elif(raw_set[4] == ' expandedLegal'):
            format = 'expanded'
        else:
            format = 'unlimited'

        this_set = {
            'id' : raw_set[8].replace('ptcgoCode','').replace(' ', '', 1),
            'name' : raw_set[6].replace('name', '').replace(' ', '', 1),
            'format' : format,
            'size' : int(raw_set[11].replace('total', '')),
            'req_id' : raw_set[0].replace('id', '').replace(' ', '', 1),
            'cards' : []
        }

        all_sets.append(this_set)
    

def req_format(format):
    global all_sets

    standard_sets = []
    expanded_sets = []
    unlimited_sets = []
    for x in all_sets:
        if (x['format'] == 'standard'):
            standard_sets.append(x)
        if (x['format'] == 'expanded'):
            expanded_sets.append(x)
        if (x['format'] == 'unlimited'):
            unlimited_sets.append(x)


    if format == 'standard':
        return standard_sets
    if format == 'expanded':
        return expanded_sets
    if format == 'unlimited':
        return unlimited_sets
    if format == 'relevant' or format == "modern":
        return standard_sets + expanded_sets
    else:
        return all_sets



def strip_card(raw_card):
    raw_card = raw_card.replace('Set', '').replace('=', '').replace('(', '').replace(')', '').replace("'",'').split(',')
    print(raw_card)
    names = []
    for item in raw_card:
        if 'supertypePokémon' in item:
            super_type = 'pokemon'

        elif 'supertypeTrainer' in item:
            super_type = 'trainer'
        else:
            super_type = 'energy'

        
        if(' name' in item):
            names.append(item.replace('name', '').replace(' ', '', 1))

        if(' subtypes' in item):
            sub_type = item.replace('subtypes[', '').replace("]", '').replace(' ', '', 1)
        
        
        if 'types[' in item:
            type = item.replace('types[', '').replace("]", '').replace(' ', '', 1)

    print(sub_type, names, type)
        

"""
WIP
"""        

raw_card = str(Card.find('xy7-36'))
strip_card(raw_card)


def get_cards(format):
    get_sets()
    sets = req_format(format)
    all_cards = []
    for set in sets:
        print(set['name'])
        count = 1

        for card in range(set['size']):
            try:
                req = str(set['req_id'] + '-' + str(count))
                raw_card = str(Card.find(req))

                print(raw_card)
                


                count +=1
            except:
                print("req error | probaly a promo set")
                break






def check_path():
    dir = os.getcwd() + '/archive/cards'

    if(os.path.exists(dir)):
        print("path found")
    else:
        os.makedirs(dir)
        print("created cards dir")

class card:
    def __init__(self, name, super_type):
        self.name = name
        self.super_type = super_type

class pokemon_card(card):
    def __init__(self, name, super_type, set, num):
        super().__init__(name, super_type)
        self.super_type = 'pokemon'
        self.set = set
        self.num = num #set num

class trainer_card(card):
    def __init__(self, name, super_type):
        super().__init__(name, super_type)
        self.super_type = 'trainer'

class energy_card(card):
    def __init__(self, name, super_type):
        super().__init__(name, super_type)
        self.super_type = 'energy'

#get_cards('standard')