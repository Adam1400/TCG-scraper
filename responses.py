import study
import scrape
import cards
import datetime


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
        query = manage_query(message)
        optimal_cards = study.get_optimal_cards(query)

        response = study.show_averages(optimal_cards) #+ study.create_decklist(optimal_cards)
        if len(response) > 300:
            return response
        else:
            return str('No results found\nsomething is up with your query ---> '+ message.split('!meta')[1])
     
    if message.startswith('!sample'):
        query = manage_query(message)
        optimal_cards = study.get_optimal_cards(query)

        response = study.create_decklist(optimal_cards)
        if len(response) > 300:
            return response
        else:
            return str('No results found\nsomething is up with your query ---> '+ message.split('!sample')[1])
     

    if message.startswith('!show'):
        query = manage_query(message)

        response = study.show_decks(query)

        if  len(response) > 10000 and '*admin' not in message:
            return str('This is going to be too big\ntighten up that query---> '+ message.split('!show')[1])

        if len(response) > 300:
            return response
        else:
            return str('No results found\nsomething is up with your query ---> '+ message.split('!show')[1])
     
    if message.startswith('!scrape'):  
        num_tournaments = -1
        top_cut = -1
        format = 'all'
        location = 'all'
        redundancy = False


        scrape.get_decks(format, num_tournaments, top_cut, location, redundancy)

        return 'Done Scraping decks'

    if message.startswith('!cards'):  
        cards.get_cards('standard')

        return 'Done Scraping cards'






def manage_query(message):

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


