import study
import scrape
import cards
import datetime
import random


def handel_responses(message) -> str:
    
    if message == 'testing':
        return 'testing'

    if message == '!help':
        response= '---------------------------------------------------------------------------------------------------------------------------------\n'
        response+= 'MAIN COMMANDS:\n'
        response+= '!meta --> gives anylitics based on card usage\n'
        response+= '!sample --> generates a sample beck based on given parameters\n'
        response+= '!show --> shows stored lists based on given parameters\n'
        response+= '\n'
        response+= 'adding a question mark "?" to the start of your command with have the bot dm you\n'
        response+= '\n'
        response+= 'PARAMETERS:\n'
        response+= 'parameters can be added to the end of any command to query down your search results\n'
        response+= 'order does not matter but each param must be comma seperated\n'
        response+= '\n'
        response+= 'deckname --> name of the deck architype\n'
        response+= 'format --> the format of the deck (standard, expanded, other, jp-standard, jp-expanded)\n'
        response+= 'topcut --> cut off of deck placement\n'
        response+= 'player --> who played the deck\n'
        response+= 'include --> what cards must be in the deck (cards must be contained in square brackets seperated by a comma [x,y,z])\n'
        response+= 'date --> minimum date cutoff (given as MM/dd/YYYY)\n'
        response+= '\n'
        response+= 'EXAMPLES:\n'
        response+= '!meta deckname=Lugia Archeops, topcut=8, date=1/1/2023\n'
        response+= '!sample include=[Beedrill,Inteleon,Cross Switcher], format=standard\n'
        response+= '!show player=Allen Adams, date=1/1/2020\n'
        response+= '--------------------------------------------------------------------------------------------------------------------------------'

        return response

    if message.startswith('!meta'):
        if '=' not in message:
            return 'add params'
        query = manage_deck_query(message)
        optimal_cards = study.get_optimal_cards(query)

        response = study.show_averages(optimal_cards) #+ study.create_decklist(optimal_cards)
        if len(response) > 300:
            return response
        else:
            return str('No results found\nsomething is up with your query ---> '+ message.split('!meta')[1])


    if message.startswith('!sample'):
        if '=' not in message:
            return 'add params'
        query = manage_deck_query(message)
        optimal_cards = study.get_optimal_cards(query)

        response = study.create_decklist(optimal_cards)
        if len(response) > 300:
            return response
        else:
            return str('No results found\nsomething is up with your query ---> '+ message.split('!sample')[1])
     

    if message.startswith('!show'):
        if '=' not in message:
            return 'add params'
        query = manage_deck_query(message)

        response = study.show_decks(query)

        if  len(response) > 10000 and '*admin' not in message:
            return str('This is going to be too big\ntighten up that query---> '+ message.split('!show')[1])

        if len(response) > 300:
            return response
        else:
            return str('No results found\nsomething is up with your query ---> '+ message.split('!show')[1])
     

    if message.startswith('!scrapedecks'): 
        if '*admin' not in message: 
            num_tournaments = -1
            top_cut = -1
            format = 'all'
            location = 'all'
            redundancy = False


            scrape.get_decks(format, num_tournaments, top_cut, location, redundancy)

            return 'Done Scraping decks'
        else:
            return 'Need to be an admin todo this'

    if message.startswith('!scrapecards'):  
        if '*admin' not in message: 

            cards.get_cards('standard')
            return 'Done Scraping cards'
        else:
            return 'Need to be an admin todo this'

    if message.startswith('!card'):  
        if '=' in message:
            response = manage_card_query(message)

            if len(response) < 5:
                return str('No results found\nsomething is up with your query ---> '+ message.split('!card')[1])

            if  len(response) > 500 and '*admin' not in message:
                return str('This is going to be too big\ntighten up that query---> '+ message.split('!card')[1])
            else:
                return response

        else:
            return 'add params to your query'


    if message.startswith('!sets'):  
        study.load_cards()
        all_cards = study.search_cards()

        return study.get_sets(all_cards)
    
    if message.startswith('!roll'):  
        dice = random.randint(1,6)

        if dice % 2 == 0:
            return str(dice)+' --> Heads'
        else:
            return str(dice)+' --> Tails'






def manage_card_query(message):

        name = ''
        set = ''
        num = 0

        study.load_cards()

        if message[-1] != ',':
            message+=','  


        if 'name=' in message:
            name = message.split('name=')[1].split(',')[0]
        if 'set=' in message:
            set= message.split('set=')[1].split(',')[0]
        if 'num=' in message:
            num= int(message.split('num=')[1].split(',')[0])
       
        query = study.search_cards(name,set,num)
        responce = study.get_card_image(query)
        return responce





def manage_deck_query(message):

        deck_name = ''
        format = ''
        top_cut = 0
        player = ''
        included_cards = ''
        date = datetime.datetime(2000, 1, 1)

        study.load_decks('all')                    
        study.load_cards()


        if message[-1] != ',':
            message+=','  


        if 'deckname=' in message:
            deck_name = message.split('deckname=')[1].split(',')[0]
        if 'format=' in message:
            format= message.split('format=')[1].split(',')[0]
        if 'topcut=' in message:
            top_cut= int(message.split('topcut=')[1].split(',')[0])
        if 'player=' in message:
            player= message.split('player=')[1].split(',')[0]
        if 'include=[' in message:
            included_cards= message.split('include=[')[1].split('],')[0]
            included_cards= included_cards.split(',')
        if 'date=' in message:
            date= message.split('date=')[1].split(',')[0]
            date_list= date.split('/')
            date = datetime.datetime(int(date_list[2]),int(date_list[0]),int(date_list[1]))


        query = study.search(
            deck_name= deck_name, 
            format= format,
            top_cut=top_cut,
            player=player,
            included_cards=included_cards, 
            date=date
            )
        
        return query


