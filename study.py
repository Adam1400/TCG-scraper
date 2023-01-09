
import os
from os import path
import hashlib
import datetime

def load_decks(path):
    #name of the folder in archive/decks
    global hashes 
    global deck_lists

    print("loading...")

    hashes = []
    raw_decks = []
    
    dir = os.getcwd() + '/archive/decks/'+path
    if(os.path.exists(dir)):
        for file in os.listdir(dir):
            print(file.split('.txt')[0])
            if (file.endswith(".txt")):
                try:
                    f = open(os.path.join(dir, file))
                    if (file == 'hashed_decks.txt'):
                        hashes = f.read().splitlines()
                        f.close()
                    else:
                        raw_decks = raw_decks + f.read().splitlines()
                        f.close()
                except:
                    print("error loading decks")
    else:
        print("no path with that name")
    print()

    if len(hashes) != 0:
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
        
        deck_lists = convert_to_dictionary(decks)
    
    else:
        deck_lists = []


def convert_to_dictionary(deck_lists):
    global decks
    print("preparing decks...")

    decks = []
    for data in deck_lists:
        cards = []
        for c in data[2:-10]:
            try: 
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
            except:
                cards = []
  
        try:
            wins = int(data[-4])
            losses =int(data[-3])
            ties = int(data[-2])
        except:
            wins = data[-4]
            losses = data[-3]
            ties = data[-2]

        deck = {
        'name' : data[0],
        'format' : data[1],
        'cards' : cards,
        'date' : datetime.datetime.strptime(data[-9],'%Y-%m-%d'),
        'event' : data[-8],
        'placement' : int(data[-7]),
        'gamer' : data[-6],
        'record' : data[-5],
        'wins' : wins,
        'losses' : losses,
        'ties' : ties,
        'id' : data[-1],
        }

        decks.append(deck)
    
    print("DONE! | retrived", len(deck_lists),"decks")
    print()
    return decks


def search(date=datetime.datetime(2000, 1, 1), player='', deck_name='', placement=0, top_cut=0, event='', id='', format=''):
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
            if(deck['gamer'] == player):
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

    if id != '':
        lists_by_id = []
        for deck in lists:
            if(deck['id'] == id):
                lists_by_id.append(deck)
            
        lists = lists_by_id

    if format != '':
        lists_by_format = []
        for deck in lists:
            if(deck['format'] == id):
                lists_by_format.append(deck)
            
        lists = lists_by_format

    return lists
    

def show_averages(query):
    unique_cards = {}
    copies = 0
    card_name = ''
    total_decks = len(query)

    for deck in query:
        for card in deck['cards']:
            copies = int(card['copies'])
            card_name = card['name']

            if card_name not in unique_cards:
                unique_cards[card_name] = copies
            else:
                unique_cards[card_name] = unique_cards[card_name] + copies


    #print(unique_cards)  

    percentage = 0

    for card in unique_cards:
    
        percentage = unique_cards[card]/total_decks
        unique_cards[card] = round(percentage, 2)


    sorted_usage = sorted(unique_cards.items(), key=lambda item: item[1], reverse=True)

    for x in sorted_usage:
        print(x)

    print(total_decks)



load_decks('test')
query = search(deck_name='Lugia Archeops',top_cut = 1, date=datetime.datetime(2022,1,1) )


show_averages(query)








"""
for deck in jc:
    print(deck['name'], "|",deck['date'])
    print(deck['record'])
    print("placement ==>",deck['placement'])
    for card in deck['cards']:
        print(card['copies'],  card['name'])
    
    
    print()

"""

        