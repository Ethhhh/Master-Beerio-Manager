#this is just testing on how to use SQLITE
#sqlite is an embedded database that does not need a server to run, or create any serpeate processes, everything runs in python itself

#initial setup for codebase

import sqlite3

connection = sqlite3.connect("C:\\Users\\ethan\\OneDrive\\Desktop\\Master Beerio Manager\\testing\\sqlitedatabasetest\\moviedb.db")
cursor = connection.cursor()

while True:
    choice = input("Press A to add a movie, U to update a movie, D to delete a movie, and L to show a list with all movies\n")

    if choice == "A": 
        name = input("Please provide a name for the movie \n")

        data = [name]
        cursor.execute("INSERT INTO 'movies' ('name') VALUES (?)", data)
        connection.commit()


    elif choice == "U":
        id = input("Please provide the ID for the movie you want to update \n")
        name = input("Please provide a name for the movie\n")

        data = [name,id]
        cursor.execute("UPDATE movies SET name=? WHERE id=?", data)
        connection.commit()

    elif choice == "D":
        id = input("Please provide the ID for the movie you want to delete \n")

        
        data = [id]
        cursor.execute("DELETE FROM movies WHERE id=?", data)
        connection.commit()

    elif choice == "L": 
        result = cursor.execute("SELECT * FROM movies")

        movies = result.fetchall()

        for movie in movies:
            print(str(movie[0])+". -"+movie[1])
        
    else:
        print("Please select a valid option and make sure it is capitalised")
        print("SCRIPT END")
        break