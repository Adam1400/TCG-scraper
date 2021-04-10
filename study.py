
import os
from os import path
import hashlib
import datetime

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
        'date' : datetime.datetime.strptime(data[-9],'%Y-%m-%d'),
        'event' : data[-8],
        'placement' : int(data[-7]),
        'gamer' : data[-6],
        'record' : data[-5],
        'wins' : int(data[-4]),
        'losses' : int(data[-3]),
        'ties' : int(data[-2]),
        'id' : data[-1],
        }

        decks.append(deck)

    return decks

        


            

print("loading...")
deck_lists = load_data('')


def search(date=datetime.datetime(2000, 1, 1), player='', deck_name='', placement=0, top_cut=0, event=''):
    global deck_lists
    lists = deck_lists
    if date != datetime.datetime(2000, 1, 1):
        lists_by_date = []
        for deck in lists:
            if(deck['date'] >= date):
                lists_by_date.append(deck)

        lists = lists_by_date
    
    if player != '':
        lists_by_player = []
        for deck in lists:
            if(deck['player'] == player):
                lists_by_player.append(deck)
        
        lists = lists_by_player

    if deck_name != '':
        lists_by_deck_name = []
        for deck in lists:
            if(deck['name'] == deck_name):
                lists_by_deck_name.append(deck)

        lists = lists_by_deck_name

    if placement != 0:
        lists_by_placement = []
        for deck in lists:
            if(deck['placement'] == placement):
                lists_by_placement.append(deck)

        lists = lists_by_placement

    if top_cut != 0:
        lists_by_top_cut = []
        for deck in lists:
            if(deck['placement'] <= top_cut):
                lists_by_top_cut.append(deck)
            
        lists = lists_by_top_cut

    if event != '':
        lists_by_event = []
        for deck in lists:
            if(deck['event'] == event):
                lists_by_event.append(deck)
            
        lists = lists_by_event

    return lists

    





    






for x in deck_lists:
    if x['date'] >= standard:
        if(x['gamer'] == 'Allen Adams'):
            print(x['name'], x['gamer'], x['record'], x['event'], x['date'])
            for card in x['cards']:
                print(card['copies'], card['name'], end=' ')
                if(card['type'] == 'pokemon'):
                    print(card['set'], card['num'])
                else:
                    print()
            print()




        