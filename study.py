
import os
from os import path
import hashlib

def load_data(path):
    global hashes 
    f = open('archive/decks/all/hashed_decks.txt')
    hashes = f.read().splitlines()
    f.close()

    d = open('archive/decks/all/standard_decks.txt')
    raw_decks = d.read().splitlines()

    deck = []
    decks = []
    count = 0
    for item in raw_decks:
        if item != '*** ':
            deck.append(item)
        else:
            decks.append(deck)
            deck = []
        count += 1
    
    return convert_to_dictionary(decks)



def convert_to_dictionary(deck_lists):
    global decks

    decks = []
    for data in deck_lists:
        cards = []
        for c in data[2:-10]:
            
            card = c.split(' ')
            copies = card[0]
            card_type = card[-1]
            card.remove(card[0])
            card.remove(card[-1])

            if(card_type == 'pokemon'):
                num = card[-1]
                set = card[-2]
                card.remove(card[-2])
                card.remove(card[-1])
                card_name = ' '.join(card)
                this_card = {
                'copies' : copies,
                'name' : card_name,
                'type' : card_type,
                'set' : set,
                'num' : num
                }
            else:
                card_name = ' '.join(card)
                this_card = {
                'copies' : copies,
                'name' : card_name,
                'type' : card_type,
                }
            
            cards.append(this_card)
  
        deck = {
        'name' : data[0],
        'format' : data[1],
        'cards' : cards,
        'date' : data[-9],
        'event' : data[-8],
        'placement' : data[-7],
        'gamer' : data[-6],
        'record' : data[-5],
        'wins' : data[-4],
        'losses' : data[-3],
        'ties' : data[-2],
        'id' : data[-1],
        }

        decks.append(deck)

    return decks

        


            

print("loading...")
deck_lists = load_data('')

for x in deck_lists:
    if x['gamer'] == 'JC Sharp':
        print(x['name'], x['gamer'], x['record'])
        for card in x['cards']:
            print(card['copies'], card['name'], end=' ')
            if(card['type'] == 'pokemon'):
                print(card['set'], card['num'])
            else:
                print()
        print()




        