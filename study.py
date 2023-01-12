import re
import os
from os import path
import hashlib
import datetime

def load_decks(path):
    #name of the folder in archive/decks
    global hashes 
    global deck_lists
    global working_deck_lists 

    print("loading decks...")
    working_deck_lists = [] 
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
        for c in data[2:-9]:
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

    global num_queried_lists
    num_queried_lists = len(lists)
    return lists
    

        

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

def get_latest_print(name, set = ''):
    cards = []
    name = name.replace("'", "")
    name = name.replace("Ã©","é")

    for card in card_lists:
        
        if set != '':
            if card["name"] == name:
                if card["set"] == set:
                    cards.append(card)
        else:
            if card["name"] == name:
                cards.append(card)
            
      
    try:
        return cards[0]# rarity -1 is max 0 is low
    except:
        return  {
        'name' : name,
        'classification' : '',
        'type': '',
        'sub_classification': '',
        'full_setname': '',
        'set': set,
        'num': '',
        'image': '',
        'id': ''
        }


def get_optimal_cards(query):
    unique_cards = {}
    optimal_cards = []
    copies = 0
    card_name = ''
    set_name = ''
    total_decks = len(query)

    for deck in query:
        if deck['name'] not in working_deck_lists:
            working_deck_lists.append(deck['name'])#set working deck lists

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


    avg = 0
    for card in unique_cards:
        avg = unique_cards[card]/total_decks
        unique_cards[card] = round(avg, 2)#decimal places in the avg


    sorted_usage = sorted(unique_cards.items(), key=lambda item: item[1], reverse=True)
    

    regex_pattern = "\((.*?)\)"
    for card in sorted_usage:
        name = card[0]
        stripped_name = name.split(" (")[0]
        count = round(total_decks* card[1])

        if count == 0:
            count  = 1

        
        try:
            stripped_set = re.findall(regex_pattern, name)[0] #try to match on set
        except:
            stripped_set = ''


        card_data = get_latest_print(stripped_name, stripped_set) 
        
        copies = int(round(card[1]))
        if copies == 0:
            copies  = 1

        single_card = {
                    'name' : stripped_name,
                    'classification' : card_data['classification'],
                    'type': card_data['type'],
                    'sub_classification': card_data['sub_classification'],
                    'full_setname': card_data['full_setname'],
                    'set': card_data['set'],
                    'num': card_data['num'],
                    'image': card_data['image'],
                    'id': card_data['id'],
                    'total_count': count,
                    'avg_count': card[1],
                    'copies': copies
                    }
    
        optimal_cards.append(single_card)

    return optimal_cards

def create_decklist(cards):
    sixty_card_deck = []
    total_count = 0

 
    for card in cards:
        total_count = total_count + int(card['copies'])
        if total_count <= 60:
                sixty_card_deck.append(card)
               
                
    pokemon = []
    trainers = []
    energy = []
    poke_count = 0
    trainer_count = 0
    energy_count = 0 


    for card in sixty_card_deck:
        if card['sub_classification'] == 'pokemon':
            pokemon.append(card)
            poke_count+=card['copies']

    for card in sixty_card_deck:
        if card['sub_classification'] == 'trainer':
            trainers.append(card)
            trainer_count+=card['copies']

    for card in sixty_card_deck:
        if card['sub_classification'] == 'energy':
            energy.append(card)
            energy_count+=card['copies']

    

    export_list = 'Pokémon: '+str(poke_count)+'\n'

    for card in pokemon:
        export_list = export_list + str(card['copies'])+ ' ' + card['name'] + ' '+ card['set'] + ' '+ str(card['num']) + '\n'
    
    export_list = export_list + '\nTrainer: '+str(trainer_count)+'\n'

    for card in trainers:
        export_list = export_list + str(card['copies'])+ ' ' + card['name'] + ' '+ card['set'] + ' '+ str(card['num']) + '\n'
    
    export_list = export_list + '\nEnergy: '+str(energy_count)+'\n'

    for card in energy:
        export_list = export_list + str(card['copies'])+ ' ' + card['name'] + ' '+ card['set'] + ' '+ str(card['num']) + '\n'

    export_list = export_list + '\nTotal Cards: '+str(poke_count+trainer_count+energy_count)


    return export_list

   
def show_averages(optimal_cards):

    for deck in working_deck_lists:
        print(deck, '|', end=' ')

    if len(working_deck_lists) > 0 :  
        print(num_queried_lists, 'Lists')
    print('---------------------------------------------------------------------')
    print('Card                                  | Avg   | total | prupose')
    print('---------------------------------------------------------------------')

    for card in optimal_cards:
        if card['avg_count'] > 0.01: ## cut out the cringe
            avg = card['avg_count']
            count = card['total_count']
            card_purpose = ''
            name = ''

            if card['sub_classification'] == 'pokemon':
                name = card['name'] +' ('+ card['set']+')'
            else:
                name = card['name']

        
            if avg <= 0.5:
                card_purpose = 'optional tech'
            if avg >= 0.5:
                card_purpose = 'required tech'
            if avg >= 2:
                card_purpose = 'consistancy'

            print(f'{name :<37} | {avg:<5} | {count:<5} | {card_purpose:<5}')

    print('---------------------------------------------------------------------') 
    print()  

def show_decks(query):
    for deck in query:
        print('----------------------------------------------')
        print(deck['name'],'|',deck['format'])
        print('')
        print('Tournament -->',deck['event'])
        print('Date Played-->', deck['date'])
        print('Record -->',deck['record'])
        print(deck['gamer'],'placed',deck['placement'])
        print('Deck ID -->',deck['id'])
        print('')

        deck_with_paired_info = []
        for card in deck['cards']:
          
            try:
                this_card = get_latest_print(card['name'], card['set'])
            except:
                this_card = get_latest_print(card['name'])

            this_card['copies'] = int(card['copies'])

            deck_with_paired_info.append(this_card)

        
        print(create_decklist(deck_with_paired_info))

        

        
        print('----------------------------------------------')
        print()


load_decks('all')                    
load_cards()


query = search(
    deck_name= 'Lost Zone Box', 
    format= 'standard',
    #top_cut=8,
    #player='ninjadrake',
    included_cards=['Reshiram'], 
    date=datetime.datetime(2023,1,1)
     )



#show_decks(query)
optimal_cards = get_optimal_cards(query)
show_averages(optimal_cards)
print(create_decklist(optimal_cards))






        







 



            
                


            


