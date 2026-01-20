#This is the first test for the elo system please read the read.me to see how to change values and optimize this sytem

############################### CONFIGURATION #####################################

k_fact = 32  ## 10 - 20 = low risk k_fact ## 32-40 = medium risk k_fact ## 50+ = high risk k_fact

#Asking for input

A = input("Who got first in the race?")
B = input("Who got second in the race?")
C = input("Who got third in the race?")
D = input("Who got fourth in the race?")


#this will be where it checks database and builds a player profile
Aprofile = [1600, A] #1 - will build UI to make this alot easier
Bprofile = [1320, B] #2
Cprofile = [1500, C] #3
Dprofile = [1400, D] #4


#functions for the rest of the code are below this line, and descriptions of wat each func is doing is also included for future reference
def expected_result():
    return 1 / ( 1 + 10 ** ((rating_B - rating_A) / 400 ))
# expected score = EA​=1/1+10^(Rb-Ra)/400

#def point_exchangeWIN():
    return k_fact * ( 1 - expectedresult) ##expected result is calculated from the expected result func

#def point_exchangeLOSS():
    return k_fact * ( 0 - expectedresult)

## BELOW THIS LINE IS ACTUAL CALCULATIONS

################################################# EXPECTED SCORE CALCULATIONS for first place #ALWAYS GO IN ABCD ORDER FOR PROPER CALUCLATIONS ONLY CHANGE DEPENDING ON RATING A
rating_B = Bprofile[0]
rating_A = Aprofile[0]
win1 = expected_result() # Player A beating Player B 

rating_B = Cprofile[0]
rating_A = Aprofile[0] # Player A beating Player C
win2 = expected_result()

rating_B = Dprofile[0]
rating_A = Aprofile[0]
win3 = expected_result()
################################################# EXPECTED SCORE CALCULATIONS for first place

################################################# EXPECTED SCORE CALCULATIONS for second place
rating_B = Aprofile[0]
rating_A = Bprofile[0]
second1 = expected_result()

rating_B = Cprofile[0]
rating_A = Bprofile[0]
second2 = expected_result()

rating_B = Dprofile[0]
rating_A = Bprofile[0]
second3 = expected_result()
################################################# EXPECTED SCORE CALCULATIONS for second place

################################################# EXPECTED SCORE CALCULATIONS for third place
rating_B = Aprofile[0]
rating_A = Cprofile[0]
third1 = expected_result()

rating_B = Bprofile[0]
rating_A = Cprofile[0]
third2 = expected_result()

rating_B = Dprofile[0]
rating_A = Cprofile[0]
third3 = expected_result()
################################################# EXPECTED SCORE CALCULATIONS for third place - We don't need one for fourth since they didnt beat anyone - this isnt true anymore cuz i changed the code

################################################# EXPECTED SCORE CALCULATIONS for fourth place
rating_B = Aprofile[0]
rating_A = Dprofile[0]
fourth1 = expected_result()

rating_B = Bprofile[0]
rating_A = Dprofile[0]
fourth2 = expected_result()

rating_B = Cprofile[0]
rating_A = Dprofile[0]
fourth3 = expected_result()
################################################# EXPECTED SCORE CALCULATIONS for fourth place


#this used to have some debug code but its gone now broken_heart

#############################################################################################################################################################################################################################################
# ELO CHANGING CALCULATIONS #

###FIRST PLACE####
EloChangeFirst1 = k_fact * ( 1 - win1 )
EloChangeFirst2 = k_fact * ( 1 - win2 )
EloChangeFirst3 = k_fact * ( 1 - win3 )

EloChangeCombined1 = EloChangeFirst1 + EloChangeFirst2 + EloChangeFirst3 
print(EloChangeFirst1)
print(EloChangeFirst2)
print(EloChangeFirst3)
print("First Place Elo Change ", EloChangeCombined1)

####SECOND PLACE######
EloChangeSecond1 = k_fact * ( 1 - second1 )
EloChangeSecond2 = k_fact * ( 1 - second2 )
EloChangeSecond3 = k_fact * ( 0 - second3 ) # since they would have lost to player A they lose some elo

EloChangeCombined2 = EloChangeSecond1 + EloChangeSecond2 + EloChangeSecond3
print(EloChangeSecond3)
print(EloChangeSecond2) # for debugging
print(EloChangeSecond1)
print("Second Place Elo Change ", EloChangeCombined2)

######THIRD PLACE #######
EloChangeThird1 = k_fact * ( 1 - third1 )
EloChangeThird2 = k_fact * ( 0 - third2 )
EloChangeThird3 = k_fact * ( 0 - third3 ) # since they would have lost to player A they lose some elo

EloChangeCombined3 = EloChangeThird1 + EloChangeThird2 + EloChangeThird3
print(EloChangeThird3)
print(EloChangeThird2) # for debugging
print(EloChangeThird1)
print("Third Place Elo Change ", EloChangeCombined3)

######FOURTH PLACE #######
EloChangeFourth1 = k_fact * ( 1 - fourth1 )
EloChangeFourth2 = k_fact * ( 0 - fourth2 )
EloChangeFourth3 = k_fact * ( 0 - fourth3 ) # since they would have lost to player A they lose some elo

EloChangeCombined4 = EloChangeFourth1 + EloChangeFourth2 + EloChangeFourth3
print(EloChangeFourth3)
print(EloChangeFourth2) # for debugging
print(EloChangeFourth1)
print("Fourth Place Elo Change ", EloChangeCombined4)