import random
import pandas as pd
import matplotlib.pyplot as plt
#these are just import for the plotting tool and some randomness
#THIS SIMULATOR IS ONLY SIMULATING 1v1v1v1's I do have logic for other races 1v1v1, 1v1, 2v2, and relays (these are a W.I.P)
# --- 1. SETTINGS ---
STARTING_ELO = 50000.0 #This is the baseline rating for every player in the simulation (The starting Elo)
K_FACTOR = 150.0 # This is the senetivity, it determines how much the points can change in each race (Remember there are technically 3 races for each race in a 1v1v1v1 (AvB, AvC, AvD))
DIVIDER = 3500.0 #Higher values make the system less punishing in a way and increase the spread of points 2000 might be an elo between (5000 - 15000) but 400 might only have a difference between (8000 - 12000)
BASE = 1.4
TOTAL_RACES = 275 # the amount of races being simulated (4 random players selected from the player array and put against eachother)

player_names = [
    "Aiden", "Alex", "Ashlin", "Brad", "Cam", "Carson", "Charlie", "Cole", 
    "Easton", "Ethan", "Ewan", "George", "Jake", "Julian", "Kaiden", 
    "Nathaniel", "Nolan", "Owen", "Rocky", "Ryley", "Santi", "Ty", "Zach"
] #every player that has attended a beerio

# Assign "Hidden Skill" (from 0.5 to 1.5) so some players naturally win more, a player with a skill rating of 1.5 is statistically more likely to outperform a player with 0.5, but it is not impossible for them to lose
skills = {"Cam": 1.5,
          "Owen": 1.45,
          "Nolan": 1.4,
          "Julian": 1.3,
          "Ethan": 1.2,
          "Kaiden": 1.1,
          "Jake":1.15,
          "Aiden": 1.0,
          "Alex": 0.95,
          "Charlie": 0.94,
          "Ryley": 0.93,
          "Rocky": 0.92,
          "Santi": 0.9,
          "Easton": 0.85,
          "Carson": 0.8,
          "Ewan": 0.78,
          "Zach": 0.75,
          "Ty": 0.72,
          "George": 0.7,
          "Cole": 0.65,
          "Ashlin": 0.6,
          "Brad": 0.55,
          "Nathaniel": 0.5} #RIGHT NOW THE SKILL RATINGS ARE BASED OFF THE GRAPH IN THE BEERIO GROUPCHAT

players = {name: {"elo": STARTING_ELO} for name in player_names} #sets up data structures, "players" stores the current rating, "history" stores the raing over time
history = {name: [STARTING_ELO] for name in player_names}

def elo_gained(ra, rb):
    return (BASE ** ((rb - ra) / DIVIDER)) * K_FACTOR

def run_simulation():
    for _ in range(TOTAL_RACES):

        matchup = random.sample(player_names, 4)
        
        # (Skill * random float determines the finishing "performance")
        performance = {p: skills[p] * random.uniform(0.8, 1.2) for p in matchup}
        results = sorted(matchup, key=lambda p: performance[p], reverse=True) # - rank players by performance (highest value = 1st place)
        
        p1, p2, p3, p4 = results
        r1, r2, r3, r4 = [players[p]['elo'] for p in results]

        #calculate the rating changes (c) - each player is compared against the other 3 they went against in the race. 
        c1 = elo_gained(r1, r2) + elo_gained(r1, r3) + elo_gained(r1, r4)

        c2 = - elo_gained(r1, r2) + elo_gained(r2, r3) + elo_gained(r2, r4)

        c3 = - elo_gained(r1, r3) - elo_gained(r2, r3) + elo_gained(r3, r4)

        c4 = - elo_gained(r1, r4) - elo_gained(r2, r4) - elo_gained(r3, r4)


        saved_points = 0 #this is a protection so that if second place is still going to lose points (for example if cole beats cam) it will cut the amount of points lost in half. it will still be net neutral as it corrects the winners score (cole) aswell
        if c2 < 0:
            original_c2 = c2
            c2 = c2 * 0.5
            saved_points = abs(original_c2 - c2)

        #this makes sure that the system is still net neutral at the end of the calculation the points that were saved from second are deducted from first
        c1 = c1 - saved_points

        #this updates the current elo ratings for the players
        players[p1]['elo'] += c1
        players[p2]['elo'] += c2
        players[p3]['elo'] += c3
        players[p4]['elo'] += c4

        #save the ratings into the history so that we can plot it on the graph
        for name in player_names:
            history[name].append(players[name]['elo'])

#simulation and visuals
run_simulation()

plt.figure(figsize=(12, 8))
#setting up the graph
for name in player_names:
    line = plt.plot(history[name], linewidth=2, alpha=0.8)
    last_y = history[name][-1]
    plt.text(len(history[name]), last_y, f"  {name}", 
             va='center', color=line[0].get_color(), fontsize=9)
#adding graph labels
plt.title("Beerlo Simulation - bruah")
plt.xlabel("Race Count")
plt.ylabel("Rating")
#show the graph
plt.show()

#this print statment just shows you the spread between the best and worst player in the python output
final_values = sorted([players[p]['elo'] for p in player_names])
print(f"range: {final_values[0]:.0f} - {final_values[-1]:.0f}")