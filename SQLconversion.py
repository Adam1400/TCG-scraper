import study
import pyodbc 
import datetime


def store_cards_in_db():
    study.load_cards()
    all_cards = study.search_cards()


    #for x in all_cards:
        #print(x)


    server = '(localdb)\Local' # Change this to the name of your local SQL Server instance
    database = 'Pokemon' # Change this to the name of your database

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')

    cursor = cnxn.cursor()

    for x in all_cards:
        hash = x['id']
        name = x['name']
        type = x['type']
        subclass = x['sub_classification']
        superclass = x['classification']
        setname = x['full_setname']
        set = x['set']
        num = x['num']
        image = x['image']

        if type == 'null type':
            type = 'NULL'
        
        if len(set) > 3:
            set = 'NULL'

        if superclass == 'subtypesNone Energy':
            superclass = 'Energy'
        
        if name == '?':
            num = 'thisshouldfail'

        
        try:
            # Insert a new row into the table
            cursor.execute("INSERT INTO Cards ([Hash], [Name], [Type], [SubClass], [SuperClass], [SetName], [Set], [Num], [Image]) VALUES ('"+hash+"', '"+name+"', '"+type+"', '"+subclass+"', '"+superclass+"', '"+setname+"', '"+set+"', '"+num+"', '"+image+"')")
            cnxn.commit()
            # Commit the transaction
            print("inserted",hash,name)
        except:
            print("failed to insert",hash,name)


    cnxn.close()







def store_decks_in_db():


    study.load_decks('all')
    all_decks = study.search()

    #all_decks = all_decks[-100:-1]




    server = '(localdb)\Local' # Change this to the name of your local SQL Server instance
    database = 'Pokemon' # Change this to the name of your database

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')

    cursor = cnxn.cursor()

    cursor.execute("select distinct [Hash] from Decks ")

    hashes = []
    rows = cursor.fetchall()
    for row in rows:
        hashes.append(str(row).replace("(","").replace(")", "").replace(",","").replace('"','').replace("'",'').replace(' ',''))

    


    deckcount = 0
    cardcount = 0
    for x in all_decks:
        hash = x['id']
        name = x['name']
        format = x['format']
        date = str(x['date'].strftime("%m/%d/%Y"))
        event = x['event']
        placement = str(x['placement'])
        player = x['gamer']
        record = x['record']
        wins = str(x['wins'])
        losses = str(x['losses'])
        ties = str(x['ties'])

        if hash not in hashes:

            if "'" in player:
                player = player.replace("'", "''")

            if "'" in name:
                name = name.replace("'", "''")
            
            if "'" in event:
                event = event.replace("'", "''")


            for card in x['cards']:
                #print(card)
                
                copies = card['copies']
                cardname= card['name']
                cardtype = card['type']

                if cardtype == 'pokemon':
                    cardset = card['set']
                    cardnum = str(card['num'])
                else:
                    cardset = 'NULL'
                    cardnum = 'NULL'


                if "'" in cardname:
                    cardname = cardname.replace("'", "''")
                try:
                    cursor.execute("INSERT INTO DeckLists ([ParentHash], [Copies], [Name], [Set], [Num], [Type]) VALUES ('"+hash+"', '"+copies+"', '"+cardname+"', '"+cardset+"', '"+cardnum+"', '"+cardtype+"')")
                    cnxn.commit()
                    cardcount+=1
                    #print("inserted card ",hash,cardname)
                except:
                    #print("failed to insert card ",hash,cardname)
                    pass
            

            
            try:
               
                # Insert a new row into the table
                cursor.execute("INSERT INTO Decks ([Hash], [Name], [Format], [Date], [Event], [Placement], [Player], [Record], [Wins], [Losses], [Ties]) VALUES ('"+hash+"', '"+name+"', '"+format+"', '"+date+"', '"+event+"', '"+placement+"', '"+player+"', '"+record+"', '"+wins+"', '"+losses+"', '"+ties+"')")
                cnxn.commit() # Commit the transaction
                print("inserted",hash,name)
                deckcount+=1
                
            
            except:
                print("failed to insert",hash,name)
                pass


    cnxn.close()
    print('inserted',deckcount,'total decks and',cardcount,'total cards')



#store_cards_in_db()
store_decks_in_db()




