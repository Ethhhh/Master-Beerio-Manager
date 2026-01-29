#make sure it always net neutral using ints
#try to make percentage based (it could be a percentage of starting ELO(10000) and that could be the k factor)
#implement guaranteed elo awards 
#implement a system to change between 1v1v1v1, 1v1v1, 1v1, 2v2s, and relays(combined team logic maybe)
#implement teammate exclusions into the team 2v2 and relay race
#implement way to track how many drinking races a player has done (This will depend on how much data we having on how many drinking vs nondrinking races we have)
#database relative path ---=--- elosim\test2\testdatabase2.db
import sqlite3
import math

connection = sqlite3.connect("elosim\\test2\\testdatabase2.db")
cursor = connection.cursor()
### FUNCTIONS ### 

def user_terminal_confirmaiton(textA):
    print(textA)
    print("Please make sure the following answers to the questions are ALWAYS the EXACT same otherwise the database will create a new entry")

def format_string(formatted_var, original_var):
    formatted_var = original_var.lower() # -- not using anymore pretty inefficent

def add_player_unique(db_path, player_name):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # The database engine handles the check for us now
            cursor.execute(
                'INSERT OR IGNORE INTO players (Name, Beerlo) VALUES (?, ?)', 
                (player_name, 10000)
            )
            
            # Check if a row was actually added

    except sqlite3.Error as e:
        print(f"Database error: {e}")

def fetch_data_db(player_Name, player_Starting_Elo ):
    cursor.execute("SELECT Beerlo FROM players WHERE Name = ?",(player_Name,))
    player_Result = cursor.fetchone()
    player_Starting_Elo = player_Result[0]
    print(player_Name, ", Starting Elo:", player_Starting_Elo)

def buildprofile(player_profile, name, elo):
    player_profile = [name, elo]
### The Program ###
# Ask player what sort of race we want
while True: 
    drinking = input("Press (D) if the race was a DRINKING race, Press (N) if the race was a NON-DRINKING race\n")
    userInput = input("Press (A) for SOLO gamemodes, Press (B) for TEAM gamemodes\n")
    if userInput == "A":
        soloInput = input("Press (A) for a 1v1v1v1, Press (B) for a 1v1v1, Press (C), for a 1v1\n")

        if soloInput == "A":
            user_terminal_confirmaiton("You are now setting up a SOLO 1v1v1v1 Race")

            soloAwinner = input("Who got first place in the race?\n")
            soloAsecond = input("Who got second place in the race?\n")
            soloAthird = input("Who got third place in the race?\n")
            soloAfourth = input("Who got last place in the race?\n")

            #format names all to lowercase(easier to manage in database)
            soloAwinnerName = soloAwinner.lower()
            soloAsecondName = soloAsecond.lower()
            soloAthirdName = soloAthird.lower()   
            soloAfourthName = soloAfourth.lower()

            #get input and format for database
            add_player_unique("elosim\test2\testdatabase2.db", soloAwinnerName)
            add_player_unique("elosim\test2\testdatabase2.db", soloAsecondName)
            add_player_unique("elosim\test2\testdatabase2.db", soloAthirdName)
            add_player_unique("elosim\test2\testdatabase2.db", soloAfourthName)
            
            ### grab data and build profile

            AwinnerProfile = [fetch_data_db(soloAwinnerName,  "dbwinnerelo")]
            fetch_data_db(soloAsecondName,  "dbsecondelo")
            fetch_data_db(soloAthirdName,  "dbthirdelo")
            fetch_data_db(soloAfourthName,  "dbfourthelo")

            

        
        elif soloInput == "B":
            user_terminal_confirmaiton("You are now setting up a SOLO 1v1v1 Race")

            soloBwinner = input("Who got first place in the race?\n")
            soloBsecond = input("Who got second place in the race?\n")
            soloCthird = input("Who got third place in the race?\n")

        elif soloInput == "C":
            user_terminal_confirmaiton("You are now setting up a SOLO 1v1 Race")

            soloCwinner = input("Who won the race?\n")
            soloCloser = input("Who lost the race?\n")

        else:
            print("Please make a valid selection and make sure it is capatalised!")
            print("Closing program (REMOVE QUIT FUNCTIONS WHEN YOU ARE FULLY DEPLOYIN THIS)")
            quit()

    elif userInput == "B":  
        teamInput = input("Press (A) for a 1v1v1v1, Press (B) for a 2v2, Press(C) for a Relay Race\n")
    
    else:
        print("Please make a valid selection and make sure it is capatalised!")
        print("Closing program (REMOVE QUIT FUNCTIONS WHEN YOU ARE FULLY DEPLOYIN THIS)")
        quit()
