import math

import sqlite3

connection = sqlite3.connect("elosim\elodatabase.db")
cursor = connection.cursor()

def add_player_unique(db_path, player_name):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # The database engine handles the check for us now
            cursor.execute(
                'INSERT OR IGNORE INTO player (Name, Beerlo) VALUES (?, ?)', 
                (player_name, 10000)
            )
            
            # Check if a row was actually added

    except sqlite3.Error as e:
        print(f"Database error: {e}")


#This is the first test for the elo system please read the read.me to see how to change values and optimize this sytem



####Connection To Database#####

FirstPlace = input("Who got first place in the race?\n")
format1 = FirstPlace.lower()

SecondPlace = input("Who got second place in the race?\n")
format2 = SecondPlace.lower()

ThirdPlace = input("Who got third place in the race?\n")
format3 = ThirdPlace.lower()

FourthPlace = input("Who got fourth place in the race?\n")
format4 = FourthPlace.lower()

#get input and format for database

add_player_unique("elosim\elodatabase.db", format1)
add_player_unique("elosim\elodatabase.db", format2)
add_player_unique("elosim\elodatabase.db", format3)
add_player_unique("elosim\elodatabase.db", format4)

###fetch from database and assign to variables
cursor.execute("SELECT Beerlo FROM player WHERE Name = ?",(format1,))
PlayerAResult = cursor.fetchone()
PlayerAStartElo = PlayerAResult[0]
print(PlayerAStartElo)

cursor.execute("SELECT Beerlo FROM player WHERE Name = ?",(format2,))
PlayerBResult = cursor.fetchone()
PlayerBStartElo = PlayerBResult[0]
print(PlayerBStartElo)

cursor.execute("SELECT Beerlo FROM player WHERE Name = ?",(format3,))
PlayerCResult = cursor.fetchone()
PlayerCStartElo = PlayerCResult[0]
print(PlayerCStartElo)

cursor.execute("SELECT Beerlo FROM player WHERE Name = ?",(format4,))
PlayerDResult = cursor.fetchone()
PlayerDStartElo = PlayerDResult[0]
print(PlayerDStartElo)



############################### CONFIGURATION ##################################### FOR 1v1v1v1

k_fact = 100  

#this will be where it checks database and builds a player profile
Aprofile = [PlayerAStartElo, format1 ] #1 - will build UI to make this alot easier
Bprofile = [PlayerBStartElo, format2] #2
Cprofile = [PlayerCStartElo, format3] #3
Dprofile = [PlayerDStartElo, format4] #4

# Updated function to accept arguments 
def expected_result(rating_player, rating_opponent):
    return 1 / (1 + 10 ** ((rating_opponent - rating_player) / 400))
#you could make another function for the fudginnn uhhh EloChangeFirst, EloChangeSecond ect.
#################################################
# CALCULATIONS
#################################################


# A vs B (Win)
win1 = expected_result(Aprofile[0], Bprofile[0])
EloChangeFirst1 = k_fact * (1 - win1)

# A vs C (Win)
win2 = expected_result(Aprofile[0], Cprofile[0])
EloChangeFirst2 = k_fact * (1 - win2)

# A vs D (Win)
win3 = expected_result(Aprofile[0], Dprofile[0])
EloChangeFirst3 = k_fact * (1 - win3)
EloChangeCombined1 = EloChangeFirst1 + EloChangeFirst2 + EloChangeFirst3 
convert1 = int(EloChangeCombined1)
print("First Place Elo Change: ", convert1)



# B vs A (Loss)
second1 = expected_result(Bprofile[0], Aprofile[0])
EloChangeSecond1 = k_fact * (0 - second1)  # Loss

# B vs C (Win)
second2 = expected_result(Bprofile[0], Cprofile[0])
EloChangeSecond2 = k_fact * (1 - second2)  # Win

# B vs D (Win)
second3 = expected_result(Bprofile[0], Dprofile[0])
EloChangeSecond3 = k_fact * (1 - second3)  # Win

EloChangeCombined2 = EloChangeSecond1 + EloChangeSecond2 + EloChangeSecond3
convert2 = int(EloChangeCombined2)
print("Second Place Elo Change: ", convert2)



# C vs A (Loss)
third1 = expected_result(Cprofile[0], Aprofile[0])
EloChangeThird1 = k_fact * (0 - third1)    # Loss

# C vs B (Loss)
third2 = expected_result(Cprofile[0], Bprofile[0])
EloChangeThird2 = k_fact * (0 - third2)    # Loss

# C vs D (Win)
third3 = expected_result(Cprofile[0], Dprofile[0])
EloChangeThird3 = k_fact * (1 - third3)    # Win

EloChangeCombined3 = EloChangeThird1 + EloChangeThird2 + EloChangeThird3
convert3 = int(EloChangeCombined3)
print("Third Place Elo Change: ", convert3)



# D vs A (Loss)
fourth1 = expected_result(Dprofile[0], Aprofile[0])
EloChangeFourth1 = k_fact * (0 - fourth1)  # Loss

# D vs B (Loss)
fourth2 = expected_result(Dprofile[0], Bprofile[0])
EloChangeFourth2 = k_fact * (0 - fourth2)  # Loss

# D vs C (Loss)
fourth3 = expected_result(Dprofile[0], Cprofile[0])
EloChangeFourth3 = k_fact * (0 - fourth3)  # Loss

EloChangeCombined4 = EloChangeFourth1 + EloChangeFourth2 + EloChangeFourth3
convert4 = int(EloChangeCombined4)
print("Fourth Place Elo Change: ", convert4)

######################## CALCULATE AND INSERT DATA INTO DATABASE #####################
PlayerAFinalElo = (PlayerAStartElo + convert1)
PlayerBFinalElo = (PlayerBStartElo + convert2)
PlayerCFinalElo = (PlayerCStartElo + convert3)
PlayerDFinalElo = (PlayerDStartElo + convert4)

cursor.execute("INSERT INTO elohistory (initialelo, finalelo, change, playername) VALUES ( ?, ?, ?, ?)", (PlayerAStartElo, PlayerAFinalElo, convert1, format1))
cursor.execute("INSERT INTO elohistory (initialelo, finalelo, change, playername) VALUES ( ?, ?, ?, ?)", (PlayerBStartElo, PlayerBFinalElo, convert2, format2))
cursor.execute("INSERT INTO elohistory (initialelo, finalelo, change, playername) VALUES ( ?, ?, ?, ?)", (PlayerCStartElo, PlayerCFinalElo, convert3, format3))
cursor.execute("INSERT INTO elohistory (initialelo, finalelo, change, playername) VALUES ( ?, ?, ?, ?)", (PlayerDStartElo, PlayerDFinalElo, convert4, format4))
connection.commit()

cursor.execute("UPDATE player SET Beerlo = ? WHERE Name = ?", (PlayerAFinalElo, format1))
cursor.execute("UPDATE player SET Beerlo = ? WHERE Name = ?", (PlayerBFinalElo, format2))
cursor.execute("UPDATE player SET Beerlo = ? WHERE Name = ?", (PlayerCFinalElo, format3))
cursor.execute("UPDATE player SET Beerlo = ? WHERE Name = ?", (PlayerDFinalElo, format4))
connection.commit()