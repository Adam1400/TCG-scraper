
import hashlib
from lxml import html
import requests
import time
import os
from os import path
import datetime
import pyodbc 



  

class tournament:
    def __init__(self, name, date, format, enteries, region, id, link):
        self.name = name
        self.date = date #Y/M/D
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
        self.date = date #Y/M/D
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
    next_page = 1
    url = 'https://play.limitlesstcg.com/tournaments/completed?time=all&show=60&game=PTCG&format=all&type=all&page=' + '1' #str(next_page)
    page = requests.get(url)
    tree = html.fromstring(page.content)

    events = []
    
    for listing in tree.xpath('//table[@class="striped completed-tournaments"]/tr'): 

        try:
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
        except:
            next_page+=1
            #url = 'https://play.limitlesstcg.com/tournaments/completed?time=all&show=499&game=PTCG&format=all&type=all&page=' + str(next_page)
            #page = requests.get(url)
            #tree = html.fromstring(page.content)


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

    url = 'https://limitlesstcg.com/tournaments?time=all&show=5'
    page = requests.get(url)
    tree = html.fromstring(page.content)
    
    #print(len(tree.xpath('//table//tr/td/a')))

    events = []
    index = 0
    for listing in tree.xpath('//table/tr/td/a'):
        if('tournaments' in listing.get('href')):
            link = 'https://limitlesstcg.com' + listing.get('href')
            id = link.split('=')[-1]
            
            format = tree.xpath('//table//img[@class="format"]')[index].get('alt').lower()
            enteries = tree.xpath('//table//td[@class="landscape-only"]/text()')[index]
            region = tree.xpath('//table//img[@class="flag"]')[index].get('alt')

            
            date = tree.xpath('//table//tr')[index+1].get('data-date')
            #print(date)
            
            names = tree.xpath('//table/tr/td/a/text()')
            names = names[::2]
            name = names[index]
            
            events.append(tournament(name, date, format, enteries, region, id, link))
            index+=1

            if index >= len(tree.xpath('//table/tr/td/a'))/2 -2:
                break

            #print(name, index)
        
    
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
        print("working on tournament", index, "/", len(tournaments), "|", event.name)
        
        url = event.link
        page = requests.get(url)
        tree = html.fromstring(page.content)


        all_deck_names = []
        for name in tree.xpath('//tr//span'):
                all_deck_names.append(name.get('data-tooltip'))

        indexofdecklist = []
        indexposition = 0
        for iodl in tree.xpath('//tr//i'):
            indexofdecklist.append(indexposition)#this part is fucked. when row has no decklist it offests the whole thing on the gamer and deckname and placement
            indexposition+=1

        deck_names = []
        for deckx in indexofdecklist:
            deck_names.append(all_deck_names[deckx])

        #print(deck_names)

   
        
        placement = 0
        for element in tree.xpath('//tr//td//a'):
            try:
                            
                if('list' in element.get('href')):
                    link = 'https://limitlesstcg.com' + element.get('href')
                    placement+=1 

                    name = deck_names[placement-1]
                    gamer = tree.xpath('//tr/td//a/text()')[placement-1]           
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

                        print("tournement",index, "| id:",id, "| saved list", placement,"| placed:", placement, '|',name)
                        save_deck_to_db(deck(id,name, deck_list, event.format, event.date, event.name, '?', placement, gamer, '?','?','?'))
                        save_deck(deck(id,name, deck_list, event.format, event.date, event.name, '?', placement, gamer, '?','?','?'))

            
                if(placement == top_cut + 1) and top_cut != -1:
                        break
            except:
                print("error retiving deck")
                
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
        print("working on tournament", index, "/", len(tournaments), "|", event.name)
        
        url = event.link
        page = requests.get(url)
        tree = html.fromstring(page.content)

        placement = 1

        deck_names = []
        
        count = 0

        #for glc
        for element in tree.xpath('//table[@class="striped"]/tr/td/a'):#glc only has a no span
            text = element.xpath('text()')
            
            if(text == ['Psychic'] or text == ['Colorless'] or text == ['Dragon'] or text == ['Darkness'] or text == ['Fire'] or text == ['Water'] or text == ['Grass'] or text == ['Lightning'] or text == ['Metal'] or text == ['Fighting'] or text == ['Fairy'] ): #skip the elements that say they dropped
                deck_names.append(element.xpath('text()')[0])
                #print(text)
            count+=1

        #for everything else
        for element in tree.xpath('//table[@class="striped"]/tr/td//span'):#they keep chaning this thing. aded span and removed modulus 7
            #print(element.xpath('text()'))
            
            if(element.xpath('text()') == []): #skip the elements that say they dropped
                if(element.get('data-tooltip') != None):
                    deck_names.append(element.get('data-tooltip'))
            count+=1

        #print(deck_names)

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
                        save_deck_to_db(deck(id, name, deck_list, format, event.date, event.name, record, placement, gamer, wins, losses, ties))
                        save_deck(deck(id, name, deck_list, format, event.date, event.name, record, placement, gamer, wins, losses, ties))
                        print("tournement",index, "| saved list", placement,"| id:",id,"|", name)

                    if(placement == top_cut):
                        break

                    placement += 1
            except:
                print("error retriving deck")
                #time.sleep(5)

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
        raw_cards = tree.xpath('//span[@class="card-name"]/text()')
        raw_copies = tree.xpath('//span[@class="card-count"]/text()')
        
        raw_set_info = tree.xpath('//a[@class="card-link"]')
        set_check = tree.xpath('//img[@class="set"]')
        
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

    try:
        f.write(str(date)+'\n')
    except:
        f.write('2000-1-1'+'\n')

    try:
        f.write(event+'\n')
    except:
        f.write('?'+'\n')
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


def save_deck_to_db(deck):
    
    server = '(localdb)\Local' # Change this to the name of your local SQL Server instance
    database = 'Pokemon' # Change this to the name of your database

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')

    cursor = cnxn.cursor()

    name = deck.name
    format = deck.format
    cards = deck.cards
        
    date = str(deck.date)
    event = deck.event
    placement = str(deck.placement)
    player = deck.gamer
    record = deck.record
    wins = str(deck.wins)
    losses = str(deck.losses)
    ties = str(deck.ties)
    hash = deck.id
    
    for card in cards:
        copies = card.copies
        cardname= card.name
        cardtype = card.type
        
        if cardtype == 'pokemon':
            cardset = card.set
            cardnum = str(card.num)
        else:
            cardset = 'NULL'
            cardnum = 'NULL'

        if "'" in cardname:
            cardname = cardname.replace("'", "''")
        try:
            cursor.execute("INSERT INTO DeckLists ([ParentHash], [Copies], [Name], [Set], [Num], [Type]) VALUES ('"+hash+"', '"+copies+"', '"+cardname+"', '"+cardset+"', '"+cardnum+"', '"+cardtype+"')")
            cnxn.commit()
            #print("inserted card ",hash,cardname)
        except:
            #print("failed to insert card ",hash,cardname)
            pass

    try:    
        # Insert a new row into the table
        cursor.execute("INSERT INTO Decks ([Hash], [Name], [Format], [Date], [Event], [Placement], [Player], [Record], [Wins], [Losses], [Ties]) VALUES ('"+hash+"', '"+name+"', '"+format+"', '"+date+"', '"+event+"', '"+placement+"', '"+player+"', '"+record+"', '"+wins+"', '"+losses+"', '"+ties+"')")
        cnxn.commit() # Commit the transaction
        #print("inserted",hash,name)     
    except:
        #print("failed to insert",hash,name)
        pass


    cnxn.close()

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

        get_sanctioned_decks(format, number_of_tournaments, top_cut, redundancy) #kinda broken some lists arent getting saved at the bottom

        get_online_decks(format, number_of_tournaments, top_cut, redundancy)


        h = open('archive/decks/'+spacifics+'hashed_decks.txt', "r")
        final = h.read().splitlines()
        h.close()

        print("Retrived", len(final) - len(start), "lists total")
        print()
    if location == 'sanctioned':
        get_sanctioned_decks(format, number_of_tournaments, top_cut, redundancy) 
    if location == 'online':
        get_online_decks(format, number_of_tournaments, top_cut, redundancy)

    


def get_db_hashes():
    server = '(localdb)\Local' # Change this to the name of your local SQL Server instance
    database = 'Pokemon' # Change this to the name of your database

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')

    cursor = cnxn.cursor()

    cursor.execute("select distinct [Hash] from Decks ")

    hashes = []
    rows = cursor.fetchall()
    for row in rows:
        hashes.append(str(row).replace("(","").replace(")", "").replace(",","").replace('"','').replace("'",'').replace(' ',''))

    return
          

    
num_tournaments = -1
top_cut = -1
format = 'all'
location = 'all'
redundancy = False


#get_decks(format, num_tournaments, top_cut, location, redundancy)











