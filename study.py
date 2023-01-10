
import os
from os import path
import hashlib
import datetime

def load_decks(path):
    #name of the folder in archive/decks
    global hashes 
    global deck_lists

    print("loading decks...")

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
        
        deck_lists = convert_decks_to_dictionary(decks)
    
    else:
        deck_lists = []


def convert_decks_to_dictionary(deck_lists):
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


def load_cards():
    global card_hashes 
    global card_lists

    print('loading cards...')

    card_hashes = []
    raw_cards = []
    
    dir = os.getcwd() + '/archive/cards'
    if(os.path.exists(dir)):
        for file in os.listdir(dir):
            print(file.split('.txt')[0])
            if (file.endswith(".txt")):
                try:
                    f = open(os.path.join(dir, file))
                    if (file == 'hashed_cards.txt'):
                        card_hashes = f.read().splitlines()
                        f.close()
                    else:
                        raw_cards = raw_cards + f.read().splitlines()
                        f.close()
                except:
                    print("error loading cards")
    else:
        print("no path with that name")
    print()
    

    if len(card_hashes) != 0:
        card = []
        cards = []
        count = 0
        for item in raw_cards:
            if item != '***':
                card.append(item)
            else:
                cards.append(card)
                card = []
            count += 1
       
        card_lists = convert_cards_to_dictionary(cards)
    
    else:
        card_lists = []

def convert_cards_to_dictionary(cards):
   
    print("preparing cards...")

    all_cards = []
    for data in cards:
        card = {
        'name' : data[0],
        'classification' : data[1],
        'type': data[2],
        'sub_classification': data[3],
        'full_setname': data[4],
        'set': data[5],
        'num': data[6],
        'image': data[7],
        'id': data[8],
        }

        all_cards.append(card)
    
    print("DONE! | retrived", len(all_cards),"cards")
    print()
    return(all_cards)
            


def search(date=datetime.datetime(2000, 1, 1), included_cards = [], player='', deck_name='', placement=0, top_cut=0, event='', id='', format=''):
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
            if(deck['format'] == format):
                lists_by_format.append(deck)
            
        lists = lists_by_format

    if included_cards != []:       
        lists = include_list_of_cards(included_cards,lists)

    return lists
    

def show_averages(query):
    unique_cards = {}
    copies = 0
    card_name = ''
    set_name = ''
    set_num = ''
    total_decks = len(query)
    deck_names = []

    for deck in query:
        if deck['name'] not in deck_names:
            deck_names.append(deck['name'])
        
        for card in deck['cards']:
            copies = int(card['copies'])
            try:
                set_name = ' (' + card['set'] +')'
                #+' '+  card['num']+')'
            except:
                set_name = ''

            card_name = card['name'] + set_name 

        


            if card_name not in unique_cards:
                unique_cards[card_name] = copies
            else:
                unique_cards[card_name] = unique_cards[card_name] + copies


    percentage = 0

    for card in unique_cards:
    
        percentage = unique_cards[card]/total_decks
        unique_cards[card] = round(percentage, 2)# round to the nearest 2 decimal 


    sorted_usage = sorted(unique_cards.items(), key=lambda item: item[1], reverse=True)

    for deck in deck_names:   
        print(deck,'|', end=' ')
    print(total_decks,'lists')
    print('---------------------------------------------------------------------')
    print('Card                                | Avg   | total | prupose')
    print('---------------------------------------------------------------------')

    name = ''
    avg = ''
    count = ''
    for card in sorted_usage:
        name = card[0]
        stripped_name = name.split(" (")[0]
        avg = str(card[1])
        count = str(round(total_decks* card[1]))
        standard_card = ''
        

        if count == '0':
            count = '1'

        if card[1] <= 0.5:
            standard_card = 'optional tech'
        if card[1] >= 0.5:
            standard_card = 'required tech'
        if card[1] >= 2:
            standard_card = 'consistancy'

        card_data = get_latest_print(stripped_name)
        sets = card_data['set']
        num = card_data['num']
        name = stripped_name + ' ('+sets+' ' +num+')'

        print(f'{name :<37} | {avg:<5} | {count:<5} | {standard_card:<5}')

     

def include_card(specific_card, query):
    filtered_lists = []
    for deck in query:
        for card in deck['cards']:
            if card['name'] == specific_card:
                filtered_lists.append(deck)
    return filtered_lists


def include_list_of_cards(list_of_contained_cards, query):

    for card in list_of_contained_cards:
       query = include_card(card,query)
       print('adding card constriant:',card ,'| Query size', len(query))
    
    print()
    return query

def get_latest_print(name):
    cards = []
    name = name.replace("'", "")
    name = name.replace("Ã©","é")
    for card in card_lists:
        if card["name"] == name:
            cards.append(card)
    try:
        return cards[-1]
    except:
        return  {
        'name' : '',
        'classification' : '',
        'type': '',
        'sub_classification': '',
        'full_setname': '',
        'set': '',
        'num': '',
        'image': '',
        'id': ''
        }



load_decks('all')
load_cards()


query = search(
    deck_name= 'Lugia Archeops', 
    top_cut=8,
    #included_cards=['Rapid Strike Urshifu V', 'Lugia V'], 
    date=datetime.datetime(2022,1,1)
     )


show_averages(query)


















        