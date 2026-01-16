# this is the initial test for the elo calculator for beerio
# the goal is for this to take user input (1st, 2mnd, 3rd, 4th) and compare against the database to award elo to the winning players and take elo away from the losing players
# to try using this script run it in an IDE and change the Elo down below to your liking :-)

import math

# --------------------
# CONFIG
# --------------------

DEFAULT_ELO = 1200
ELO_BASE = 400
K_NEW = 40

# --------------------
# PLAYER MODEL
# --------------------

class Player:
    def __init__(self, name):
        self.name = name
        self.elo = DEFAULT_ELO
        self.races = 0

    def __repr__(self):
        return f"{self.name}: {self.elo:.1f}"

# --------------------
# ELO FUNCTIONS
# --------------------

def expected_score(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / ELO_BASE))

def elo_delta(rating_a, rating_b, score_a):
    expected = expected_score(rating_a, rating_b)
    return K_NEW * (score_a - expected)

# --------------------
# FREE FOR ALL (1v1v1v1)
# --------------------

def process_ffa_race(finish_order):
    """
    finish_order: list of Player objects from 1st -> last
    """
    changes = {p: 0 for p in finish_order}

    for i in range(len(finish_order)):
        for j in range(i + 1, len(finish_order)):
            winner = finish_order[i]
            loser = finish_order[j]

            delta = elo_delta(winner.elo, loser.elo, 1)

            changes[winner] += delta
            changes[loser] -= delta

    # normalize by number of opponents
    for p in changes:
        changes[p] /= (len(finish_order) - 1)

    # apply changes
    for p in finish_order:
        p.elo += changes[p]
        p.races += 1

# --------------------
# TEST
# --------------------

A = Player("Ethan")
B = Player("Alex")
C = Player("Owen")
D = Player("Jewee")

players = [A, B, C, D]

print("Before race:")
for p in players:
    print(p)

# Fake race result
finish_order = [B, A, D, C]

process_ffa_race(finish_order)

print("\nAfter race:")
for p in players:
    print(p)
