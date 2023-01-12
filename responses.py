import study

def handel_responses(message) -> str:
    
    if message == 'testing':
        return 'testing'

    if message == '!help':
        return "fill this out later"

    if message == '!GetList':
        study.load_decks('all')                    
        study.load_cards()


        query = study.search(
            #deck_name= 'Lost Zone Box', 
            #format= 'standard',
            top_cut=8,
            player='Allen Adams',
            #included_cards=['Reshiram'], 
            #date=datetime.datetime(2023,1,1)
            )



        optimal_cards = study.get_optimal_cards(query)
        return study.create_decklist(optimal_cards)


