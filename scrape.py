
import hashlib
from lxml import html
import requests
import time
import os
from os import path

from requests.models import DEFAULT_REDIRECT_LIMIT

  

class tournament:
    def __init__(self, name, date, format, enteries, region, id, link):
        self.name = name
        self.date = date
        self.format = format
        self.enteries = enteries
        self.region = region # online is region
        self.id = id # can either be a name or url id
        self.link = link # url to standings


class deck:
    def __init__(self, id, name, cards, format, date, event, record, placement, gamer, wins, losses, ties):
        self.id = id# unique hash of the deck
        self.name = name
        self.cards = cards
        self.format = format
        self.date = date
        self.event = event
        self.record = record # 0-0-0 format
        self.placement = placement
        self.gamer = gamer # player name
        self.wins = wins # given as list of deck names
        self.losses = losses 
        self.ties = ties


class card:
    def __init__(self, name, copies, type):
        self.name = name
        self.copies = copies # copies played in deck
        self.type = type
        
class pokemon_card(card):
    def __init__(self, name, copies, type, set, num):
        super().__init__(name, copies, type)
        self.set = set
        self.num = num #set num

class trainer_card(card):
    def __init__(self, name, copies, type):
        super().__init__(name, copies, type)

class energy_card(card):
    def __init__(self, name, copies, type):
        super().__init__(name, copies, type)

         
def get_online_tournaments(request_format, number_of_tournys):
    #-1 number_of_tournys returns all tourny 
    
    print("fetching online tournament list...")

    url = 'https://play.limitlesstcg.com/tournaments/completed?time=all'
    page = requests.get(url)
    tree = html.fromstring(page.content)

    events = []
    
    for listing in tree.xpath('//table[@class="striped completed-tournaments"]/tr'): 
        name = str(listing.get('data-name'))
        date = str(listing.get('data-date')).split('T')[0].rstrip()
        format = str(listing.get('data-format'))
        enteries = str(listing.get('data-players'))
        region = "online"
        id = ''
        link = ''

        if(format == "4"):
            format = "standard"
        elif(format == "3"):
            format = "expanded"
        else:
            format = "other"
           
        events.append(tournament(name, date, format, enteries, region, id, link))

    events.pop(0) # blank indexed at 0
    
    count = 0
    for listing in tree.xpath('//table[@class="striped completed-tournaments"]/tr/td/a[@class="date"]'):
        id = str(listing.get('href')).split('/')[2].lstrip()
        link = 'https://play.limitlesstcg.com' + str(listing.get('href'))

        events[count].id = id
        events[count].link = link

        count+=1

    
    if(request_format != "all"):
        count = 0
        requested = []
        for x in events:
            if(x.format == request_format):
                requested.append(x)

            count+=1
        events = requested
    
    if(number_of_tournys == -1):
        number_of_tournys = len(events)

    if(number_of_tournys <= len(events) and number_of_tournys > 0):
        return events[0:number_of_tournys]

    
    return events

def get_sanctioned_tournements(request_format, number_of_tournys):
    #-1 number_of_tournys returns all tourny 
    
    print("fetching sanctioned tournament list...")

    url = 'https://limitlesstcg.com/tournaments/?time=all'
    page = requests.get(url)
    tree = html.fromstring(page.content)

    events = []
    index = 0
    for listing in tree.xpath('//table/tr/td/a'):
        if('tournaments' in listing.get('href')):
            link = 'https://limitlesstcg.com' + listing.get('href')
            id = link.split('=')[-1]
            
            format = tree.xpath('//table/tr/td/span/img[@class="formaticon"]')[index].get('alt').lower()
            enteries = tree.xpath('//table/tr/td[@class="hidden-xs show-landscape"]/text()')[index]
            region = tree.xpath('//table/tr/td/span/img[@class="flagicon"]')[index].get('alt')

            dates = names = tree.xpath('//table/tr/td/text()')
            dates = dates[::2]
            raw_date = dates[index].split(' ')
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            raw_date[1]
            month = months.index(raw_date[1])

            date = "20"+str(raw_date[-1])+"-"+str(month+1)+"-"+str(raw_date[0])

            names = tree.xpath('//table/tr/td/a/text()')
            names = names[::2]
            name = names[index]
            
            events.append(tournament(name, date, format, enteries, region, id, link))
            index+=1
        
    
    if(request_format != "all"):
        count = 0
        requested = []
        for x in events:
            if(x.format == request_format):
                requested.append(x)

            count+=1
        events = requested

    if(number_of_tournys == -1):
        number_of_tournys = len(events)

    if(number_of_tournys <= len(events) and number_of_tournys > 0):
        return events[0:number_of_tournys]

    return events

def get_sanctioned_decks(tournamanet_format, num_tournaments, top_cut, redundancy):
    #top_cut -1 gets all lists
    tournaments = get_sanctioned_tournements(tournamanet_format, num_tournaments)

    print("Got", len(tournaments), "tournaments!")

    h = open('archive/decks/'+spacifics+'hashed_decks.txt', "r")
    check = h.read().splitlines()
    h.close()

    index = 1
    for event in tournaments:

        print()
        print("working on tournament", index)
        
        url = event.link
        page = requests.get(url)
        tree = html.fromstring(page.content)

        deck_names = []
        for name in tree.xpath('//tr/td/span'):
            deck_names.append(name.get('title'))
            
        deck_names.pop(0)
        deck_names = deck_names[::2]
        
        placement = 0
        for element in tree.xpath('//tr/td/a'):
            try:
                if('/ranking/?' in element.get('href')):
                    placement+=1 
                    
                            
                if('list' in element.get('href')):
                    link = 'https://limitlesstcg.com' + element.get('href')
                    
                    name = deck_names[placement-1]
                    gamer = tree.xpath('//tr/td/a/text()')[placement-1]           
                    deck_list = scrape_list(event.region, link)
                    record = '?'
                    id = hash_deck(link, name, deck_list, gamer, record)
                   

                    if(id in check):
                        if(redundancy == False):
                            print("redundant deck found | skipping tournament")
                            break
                        else:
                            print("redundant deck found | id:", id)
                    else:

                        print("tournement",index, "| saved list", placement, "| id:",id)
                        save_deck(deck(id,name, deck_list, event.format, event.date, event.name, '?', placement, gamer, '?','?','?'))

            
                if(placement == top_cut + 1):
                        break
            except:
                print("error retiving deck")
                time.sleep(5)
        
        index+=1

    h = open('archive/decks/'+spacifics+'hashed_decks.txt', "r")
    final = h.read().splitlines()
    h.close()

    print()
    print("Complete! | retrived", len(final) - len(check), "deck lists (sanctioned)")
    print()
    
      
def get_online_decks(tournamanet_format, num_tournaments, top_cut, redundancy):
    #top_cut -1 gets all lists
    global spacifics
    tournaments = get_online_tournaments(tournamanet_format, num_tournaments)

    print("Got", len(tournaments), "tournaments!")

    h = open('archive/decks/'+spacifics+'hashed_decks.txt', "r")
    check = h.read().splitlines()
    h.close()

    index = 1
    for event in tournaments:
        print()
        print("working on tournament", index)
        
        url = event.link
        page = requests.get(url)
        tree = html.fromstring(page.content)

        placement = 1

        deck_names = []
        
        count = 0
        for element in tree.xpath('//table[@class="striped"]/tr/td'):
            if(count // 7):
                if(element.get('title') != None):
                    deck_names.append(element.get('title'))
            count+=1

        deck_records = []
        w = []
        l = []
        t = []
        for x in tree.xpath('//table[@class="striped"]/tr/td/text()'):
            if '-' in x:
                deck_records.append(x.replace(' ', ''))

                w.append(x.replace(' ', '').split("-")[0])
                l.append(x.replace(' ', '').split("-")[1])
                t.append(x.replace(' ', '').split("-")[2])
                

        gamers = []
        for x in tree.xpath('//table[@class="striped"]/tr'):
            gamers.append(x.get('data-name'))

        region = event.region
        for player in tree.xpath('//table[@class="striped"]/tr/td/a'):
            try:
                if('/decklist' in player.get('href')):
                    link = ('https://play.limitlesstcg.com'+ player.get('href'))
                    
                    deck_list = scrape_list(region, link)
                    name = deck_names[placement-1]
                    format = event.format
                    record = deck_records[placement-1]
                    gamer = gamers[placement]
                    wins = w[placement-1]
                    losses = l[placement-1]
                    ties = t[placement-1]
                    id = hash_deck(link, name, deck_list, gamer, record)

                    if(id in check):
                        if(redundancy == False):
                            print("redundant deck found | skipping tournament")
                            break
                        else:
                            print("redundant deck found | id:", id)
                    else:
                        save_deck(deck(id, name, deck_list, format, event.date, event.name, record, placement, gamer, wins, losses, ties))
                        print("tournement",index, "| saved list", placement, "| id:",id)

                    if(placement == top_cut):
                        break

                    placement += 1
            except:
                print("error retriving deck")
                time.sleep(5)

        index +=1

    h = open('archive/decks/'+spacifics+'hashed_decks.txt', "r")
    final = h.read().splitlines()
    h.close()

    print()
    print("Complete! | saved", len(final) - len(check), "deck lists (online)")
    print()

def scrape_list(region, url):
    #returns list of cards
    page = requests.get(url)
    tree = html.fromstring(page.content) 

    deck_list = []

    if (region == 'online'): 
        #strictly for scraping online tournements 
             
        raw_cards = tree.xpath('//div[@class="cards"]/p/a/text()')

        
        card_type = ""
        for card in raw_cards:
            card_data = card.split(' ')
            copies = card_data[0]
            card_data = card_data[1:]
            
            if "(" in card_data[-1] and ")" in card_data[-1]:
                set_data = card_data[-1].strip(")").lstrip("(").split("-")
                set = set_data[0]
                num = set_data[-1]
                card_type = "pokemon"
                card_data.remove(card_data[-1])
            else:
                set = ''
                num = ''
                if("Energy" in card_data):
                    card_type = "energy"
                else:
                    card_type = "trainer"

            name = ' '.join(card_data)

            
            if(card_type == "pokemon"):
                deck_list.append(pokemon_card(name,  copies, card_type, set, num))
        
            if(card_type == "trainer"):
                deck_list.append(trainer_card(name, copies, card_type))

            if(card_type == "energy"):
                deck_list.append(energy_card(name, copies, card_type))
        

    else:
        #scraping sanctioned tourny
        raw_cards = tree.xpath('//span[@class="decklist-card-name"]/text()')
        raw_copies = tree.xpath('//span[@class="decklist-card-count"]/text()')
        
        raw_set_info = tree.xpath('//div[@class="decklist-column"]/p/a')
        set_check = tree.xpath('//div[@class="decklist-column"]/p/a/span/img')
        
        sets = []
        nums = []
        for x in raw_set_info:
            if('/cards/' in x.get('href')):
                info = x.get('href')
                info = info.split('/')
                info.remove(info[0])
                info.remove(info[-1])
                info.remove('cards')
                nums.append(info[-1])
                info.remove(info[-1])
                sets.append(' '.join(info))
        
        count = 0
        for card in raw_cards:
            name = card
            copies = raw_copies[count]


            if(count < len(set_check)):
                type = 'pokemon'
                set = sets[count]
                num = nums[count]

                deck_list.append(pokemon_card(name, copies, type, set, num))

            else:
                if('Energy' in name):
                    type = 'energy'
                    deck_list.append(energy_card(name, copies, type))
                else:
                    type = 'trainer'
                    deck_list.append(trainer_card(name, copies, type))
            
            count +=1
        

    check_decklist(deck_list)
    return deck_list


def check_decklist(deck):
    card_count = 0
    for card in deck:
        card_count = card_count + int(card.copies)

    if card_count == 60:
        return

def hash_tournament(link, name, date, enterys):
    pre = link + name + date + str(enterys)
    return hashlib.sha1(str.encode(pre)).hexdigest()[0:10]

def hash_deck(link, name, deck, gamer, record):
    #create a hash for a unique deck instance 
    pre = link + name + gamer + record
    for card in deck:
        pre = pre + card.name + str(card.copies)

    return hashlib.sha1(str.encode(pre)).hexdigest()[0:10]


def save_deck(deck):
    global spacifics

    name = deck.name
    format = deck.format
    cards = deck.cards
        
    date = deck.date
    event = deck.event
    placement = deck.placement
    gamer = deck.gamer
    record = deck.record
    wins = deck.wins
    losses = deck.losses
    ties = deck.ties
    id = deck.id
    

    

    h = open('archive/decks/'+spacifics+'hashed_decks.txt', "a")
    h.write(str(id)+'\n')
    h.close()

    f = open('archive/decks/'+spacifics+format+'_decks.txt', "a")

    f.write(name +'\n')
    f.write(format+'\n')
    for card in cards:
        try:
            f.write(card.copies +" "+ card.name)
        except:
            f.write(card.copies + " ?")
        try:
            f.write(" "+ card.set +" "+ card.num +" "+card.type+ "\n")
        except:
            f.write(" "+ card.type+'\n')
    f.write(date+'\n')
    f.write(event+'\n')
    f.write(str(placement)+'\n')
    try:
        f.write(gamer+'\n')
    except:
        f.write('?'+'\n')
    f.write(record+'\n')
    f.write(wins+'\n')
    f.write(losses+'\n')
    f.write(ties+'\n')
    f.write(id+'\n')
    f.write("*** \n")
    f.close()

def check_path():
    global spacifics
    global top_cut

    if(top_cut != -1):
        spacifics = 'top' + str(top_cut)+ '/'
        sub_der = 'top' + str(top_cut)
    else:
        spacifics = 'all/'
        sub_der = 'all'

    if(path.exists('archive/decks/'+spacifics+'hashed_decks.txt')):
        print("path found")
    else:
        dir = os.getcwd() + '/archive/decks/'+sub_der
        os.makedirs(dir)
        open('archive/decks/'+spacifics+'hashed_decks.txt', "w")
        
def get_decks(format, number_of_tournaments, top_cut, location, redundancy):
    """
    format => all, expanded, standard, other, jp-standard, jp-exoanded
    number_of_tournaments = > -1 == all
    top_cut => -1 == all lists
    location ==> all, online, sanctioned 
    """
    check_path()

    if location == 'all':
        h = open('archive/decks/'+spacifics+'hashed_decks.txt', "r")
        start = h.read().splitlines()
        h.close()

        get_online_decks(format, number_of_tournaments, top_cut, redundancy)
        get_sanctioned_decks(format, number_of_tournaments, top_cut, redundancy) 

        h = open('archive/decks/'+spacifics+'hashed_decks.txt', "r")
        final = h.read().splitlines()
        h.close()

        print("Retrived", len(final) - len(start), "lists total")
        print()
    if location == 'sanctioned':
        get_sanctioned_decks(format, number_of_tournaments, top_cut, redundancy) 
    if location == 'online':
        get_online_decks(format, number_of_tournaments, top_cut, redundancy)

    


        

    
num_tournaments = -1
top_cut = -1
format = 'all'
location = 'all'
redundancy = False

get_decks(format, num_tournaments, top_cut, location, redundancy)
get_decks(format, num_tournaments, 8, location, redundancy)
get_decks(format, num_tournaments, 1, location, redundancy)










