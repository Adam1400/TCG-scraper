import os
from dotenv import load_dotenv
import time
import hashlib

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
            'size' : int(raw_set[-2].replace('total', '')),
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



def strip_card(raw_card, count, set_id):
    raw_card = raw_card.replace('Set', '').replace('=', '').replace('(', '').replace(')', '').replace("'",'').split(',')
    names = []
    for item in raw_card:

        num = count
        set = set_id

        if 'supertypePokémon' in item or 'supertypePokemon' in item:
            super_type = 'pokemon'

        if 'supertypeTrainer' in item:
            super_type = 'trainer'
        if 'supertypeEnergy' in item:
            super_type = 'energy'

        
        if(' name' in item):
            #should return card name and full set name
            names.append(item.replace('name', '').replace('"', '').replace(' ', '', 1))


        if(' subtypes' in item):
            #such as basic, stage 2, plasma
            sub_type = item.replace('subtypes[', '').replace("]", '').replace(' ', '', 1)
        
        
        if 'types[' in item:
            #such ass grass fire water
            type = item.replace('types[', '').replace("]", '').replace(' ', '', 1)

        if ' largehttps://' in item:
            image = item.replace('large', '').replace("]", '').replace(' ', '', 1)
        
    
    if('text' in names[0]):
        names[0] = names[1]
        try:
            if('flavortext' in names[0]):
                names[0] = names[2]
        except:
            names[0] = '?'

    if(len(names[0]) > 50):
        names[0] = '?'

    if(super_type == 'energy'):
        sub_type = sub_type+' Energy'

    hash = hash_card(image, names[0], set, num)

    if(super_type == 'pokemon'):
        this_card = {
        'name' : names[0],
        'subtype' : sub_type,
        'type' : type,
        'supertype' : super_type,
        'setname' : names[1],
        'set' : set,
        'num' : num,
        'image' : image,
        'hash' : hash
        }
    if(super_type == 'trainer'):
        this_card = {
        'name' : names[0],
        'subtype' : sub_type,
        'supertype' : super_type,
        'setname' : names[1],
        'set' : set,
        'num' : num,
        'image' : image,
        'hash' : hash
        }
    if(super_type == 'energy'):
        this_card = {
        'name' : names[0],
        'subtype' : sub_type,
        'supertype' : super_type,
        'setname' : names[1],
        'set' : set,
        'num' : num,
        'image' : image,
        'hash' : hash
        }
    
    return this_card


def get_cards(format):
    get_sets()
    sets = req_format(format)

    check_path()
    h = open('archive/cards/hashed_cards.txt', "r")
    check = h.read().splitlines()
    h.close()

    for set in sets:
        print(set['name'])
        count = 1

        for card in range(set['size']):
            try:
                req = str(set['req_id'] + '-' + str(count))
                raw_card = str(Card.find(req))

                card = strip_card(raw_card, count, set['id'])
                
                if(card['hash'] in check):
                    print('found redundant card | skipping set')
                    break

                save_card(card)
                print(set['id'], count,"| saved to", card['supertype'],"|", card['hash'], "|", card['name'])
                

                count +=1
            except:
                print("req error | probaly a promo set")
                time.sleep(2)
                break

        print()


def hash_card(image, name, set, num):
    #create a hash for a unique card instance 
    pre = image + name + set + str(num)
    return hashlib.sha1(str.encode(pre)).hexdigest()[0:10]
    
def check_path():
    dir = os.getcwd() + '/archive/cards'
    sub = '/hashed_cards.txt'

    if(os.path.exists(dir+sub)):
        print("found existing cards archive")
    else:
        try:
            os.makedirs(dir)
            print("created cards dir")
        except:
            print('creating hashed_cards.txt')
        open(dir+sub, "w")


def save_card(card):
    name = card['name']
    subtype = card['subtype']
    supertype = card['supertype']
    setname =  card['setname']
    set = card['set']
    num = str(card['num'])
    image = card['image']
    hash = card['hash']
    try:
        type = card['type']
    except:
        type = 'null type'
    
    this_card = [name, subtype, type, supertype, setname, set, num, image, hash, '***']

    f = open('archive/cards/'+supertype+'_cards.txt', "a")

    for item in this_card:
        try:
            f.write(item+'\n')
        except:
            f.write('?\n')
    
    f.close()

    h = open('archive/cards/hashed_cards.txt', "a")
    h.write(str(hash)+'\n')
    h.close()

    
get_cards('standard')