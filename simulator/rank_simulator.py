import random
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. SETTINGS ---
STARTING_ELO = 10000.0
K_FACTOR = 250.0
DIVIDER = 1200.0  
TOTAL_RACES = 200 

player_names = [
    "Aiden", "Alex", "Ashlin", "Brad", "Cam", "Carson", "Charlie", "Cole", 
    "Easton", "Ethan", "Ewan", "George", "Jake", "Julian", "Kaiden", 
    "Nathaniel", "Nolan", "Owen", "Rocky", "Ryley", "Santi", "Ty", "Zach"
]

# Assign "Hidden Skill" (from 0.5 to 1.5) so some players naturally win more
skills = {"Cam": 1.5,
          "Owen": 1.45,
          "Nolan": 1.4,
          "Julian": 1.3,
          "Ethan": 1.2,
          "Kaiden": 1.1,
          "Jake":1.05,
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
          "Nathaniel": 0.5}
players = {name: {"elo": STARTING_ELO} for name in player_names}
history = {name: [STARTING_ELO] for name in player_names}

def expected_result(ra, rb):
    return 1 / (1 + 10 ** ((rb - ra) / DIVIDER))

def run_simulation():
    for _ in range(TOTAL_RACES):

        matchup = random.sample(player_names, 4)
        
        # (Skill * random factor determines the finishing "performance")
        performance = {p: skills[p] * random.uniform(0.8, 1.2) for p in matchup}
        results = sorted(matchup, key=lambda p: performance[p], reverse=True)
        
        p1, p2, p3, p4 = results
        r1, r2, r3, r4 = [players[p]['elo'] for p in results]


        c1 = K_FACTOR * ((1-expected_result(r1,r2)) + (1-expected_result(r1,r3)) + (1-expected_result(r1,r4)))

        c2 = K_FACTOR * ((0-expected_result(r2,r1)) + (1-expected_result(r2,r3)) + (1-expected_result(r2,r4)))

        c3 = K_FACTOR * ((0-expected_result(r3,r1)) + (0-expected_result(r3,r2)) + (1-expected_result(r3,r4)))

        c4 = K_FACTOR * ((0-expected_result(r4,r1)) + (0-expected_result(r4,r2)) + (0-expected_result(r4,r3)))


        saved_points = 0 #this is a protection so that if second place is still going to lose points (for example if cole beats cam) it will cut the amount of points lost in half. it will still be net neutral as it corrects the winners score (cole) aswell
        if c2 < 0:
            original_c2 = c2
            c2 = c2 * 0.5
            saved_points = abs(original_c2 - c2)

        c1 = c1 - saved_points


        players[p1]['elo'] += c1
        players[p2]['elo'] += c2
        players[p3]['elo'] += c3
        players[p4]['elo'] += c4


        for name in player_names:
            history[name].append(players[name]['elo'])


run_simulation()

plt.figure(figsize=(12, 8))

for name in player_names:
    line = plt.plot(history[name], linewidth=2, alpha=0.8)
    last_y = history[name][-1]
    plt.text(len(history[name]), last_y, f"  {name}", 
             va='center', color=line[0].get_color(), fontsize=9)

plt.title("Beerlo Simulation - End-of-Line Labels")
plt.xlabel("Race Count")
plt.ylabel("Rating")
plt.show()