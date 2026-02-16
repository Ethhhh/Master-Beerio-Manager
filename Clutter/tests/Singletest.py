K_FACTOR = 75
DIVIDER = 3000
BASE = 1.4

r1 = float(input("Please enter the BKR of the 1st place racer:"))
r2 = float(input("Please enter the BKR of the 2nd place racer:"))
r3 = float(input("Please enter the BKR of the 3rd place racer:"))
r4 = float(input("Please enter the BKR of the 4th place racer:"))

def elo_gained(ra, rb):
    return (BASE ** ((rb - ra) / DIVIDER)) * K_FACTOR

u1 = round(r1 + elo_gained(r1, r2) + elo_gained(r1, r3) + elo_gained(r1, r4),1)
u2 = round(r2 - elo_gained(r1, r2) + elo_gained(r2, r3) + elo_gained(r2, r4),1)
u3 = round(r3 - elo_gained(r1, r3) - elo_gained(r2, r3) + elo_gained(r3, r4),1)
u4 = round(r4 - elo_gained(r1, r4) - elo_gained(r2, r4) - elo_gained(r3, r4),1)

print("The BKR of the 1st place racer has updated from: " + str(r1) + " to: " + str(u1))
print("The BKR of the 2nd place racer has updated from: " + str(r2) + " to: " + str(u2))
print("The BKR of the 3rd place racer has updated from: " + str(r3) + " to: " + str(u3))
print("The BKR of the 4th place racer has updated from: " + str(r4) + " to: " + str(u4))