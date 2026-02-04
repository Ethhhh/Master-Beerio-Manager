
#This is the first test for the elo system please read the read.me to see how to change values and optimize this sytem

############################### CONFIGURATION ##################################### FOR 1v1v1v1

k_fact = 100  ## 10 - 20 = low risk k_fact ## 32-40 = medium risk k_fact ## 50+ = high risk k_fact IGNORE THIS IS NOT RELEVANT TO THE CURRENT NUMBERS

#Asking for input

A = input("Who got first in the race?")
B = input("Who got second in the race?")
C = input("Who got third in the race?")
D = input("Who got fourth in the race?")


#this will be where it checks database and builds a player profile
Aprofile = [10000, A] #1 - will build UI to make this alot easier
Bprofile = [10000, B] #2
Cprofile = [10000, C] #3
Dprofile = [10000, D] #4

# Updated function to accept arguments 
def expected_result(rating_player, rating_opponent):
    return 1 / (1 + 10 ** ((rating_opponent - rating_player) / 400))
#you could make another function for the fudginnn uhhh EloChangeFirst, EloChangeSecond ect.
#################################################
# CALCULATIONS
#################################################

# --- FIRST PLACE (Beats B, C, D) ---
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
print("First Place Elo Change: ", EloChangeCombined1)


# --- SECOND PLACE (Lost to A; Beats C, D) ---
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
print("Second Place Elo Change: ", EloChangeCombined2)


# --- THIRD PLACE (Lost to A, B; Beats D) ---
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
print("Third Place Elo Change: ", EloChangeCombined3)


# --- FOURTH PLACE (Lost to A, B, C) ---
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
# FIXED: Variables below were printing "Third3", "Third2", etc.
print("Fourth Place Elo Change: ", EloChangeCombined4)