#initial setup for codebase

import sqlite3
import math



# test 2 for elo system

Initial_Elo = 1500
Elo_base = 400
K_FACTOR = 32

# Base values for calculation 

players = ["Cam", "Ethan", "Owen", "Ty"]
playerid = [1,2,3,4]
elorating = [1500, 1400, 1300, 1000]

# player data from database

playerprofile = []

for name, pid, elo in zip(players, playerid, elorating):
    playerprofile.append({
        "name": name,
        "id": pid,
        "elo": elo
    })


