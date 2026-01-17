#setup for reading and writing to database

import sqlite3

connection = sqlite3.connect("C:\\Users\\ethan\\OneDrive\\Desktop\\Master Beerio Manager\\beeriodatabase\\beeriodatabase.db")
cursor = connection.cursor()

while True:
    selection = input("Press A to add beerio history to the database, Press B to view all beerio history, Press C to find a beerio by ID, Press D to change previous beerio data\n")

    if selection == "A":
        game = input("What game did you play? (Please type the full name + CC if needed)\n")
        winner = input("Who won the tournament?\n")
        second = input("Who got 2nd place in the tournament?\n")
        third = input("Who got 3rd place in the tournament?\n")
        fourth = input("Who got 4th place in the tournament?\n")
        date = input("What month/year way this beerio? Please enter in this format(September/2025)")

        data = [game,winner,second,third,fourth,date]
        cursor.execute("INSERT INTO 'event' ('game', 'winner', '2nd', '3rd', '4th', 'date') VALUES (?, ?, ?, ?, ?, ?)", data)
        connection.commit()

        print("Data succesfully added to the Beerio database!")
    
    else:
        print("I have not finished this code yet")   
        break