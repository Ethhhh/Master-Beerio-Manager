import streamlit as st
import pandas as pd
import sqlite3 as sqlite
import math
import time
connection = sqlite.connect("streamlit\\databasetesting\\databasetest1.db")
cursor = connection.cursor()

#database logic

def addUniquePlayer(player_name):
    try:
        with sqlite.connect("streamlit\\databasetesting\\databasetest1.db") as conn:
            cursor = conn.cursor()


            cursor.execute(
                'INSERT OR IGNORE INTO players (Name, Beerlo, Drinking_Races, Beerios_Attended, Beerios_Won, Races_Done) VALUES (?, ?, ?, ?, ?, ?)', 
                (player_name, 10000, 0, 0, 0, 0)
            )
            
            print(player_name, "Check/Added to Database!")


    except sqlite.Error as e:
        print(f"Database error: {e}")


def fetchPlayerData(player_Name):

    with sqlite.connect("streamlit\\databasetesting\\databasetest1.db") as conn:
        cursor = conn.cursor()
        
        query = """
        SELECT Name, Beerlo, Drinking_Races, Races_Done
        FROM players
        WHERE Name = ?
        """
        cursor.execute(query, (player_Name,))
        result = cursor.fetchone()

        # 2. Check result
        if result:
            player_Stats = {
                "Name": result[0],
                "Beerlo": result[1],
                "Drinking_Races": result[2],
                "Races_Done": result[3],
            }
            return player_Stats
        else:

            print(f"DEBUG: Could not find {player_Name} in database.")
            return None

def expected_result(rating_player, rating_opponent):
    """Calculates the probability of winning (0.0 to 1.0)"""
    return 1 / (1 + 10 ** ((rating_opponent - rating_player) / 400))


st.logo = ("") #
st.title("Log Races")
st.badge("Testing", color="yellow")


players = ["Cam", "Nolan", "Owen", "Julian", "Ethan", "Kaiden", "Jake", "Alex", "Aiden", "Easton", "Charlie", "Ryley", "Rocky", "Ty", "Santi", "Ewan", "Carson", "George", "Brad", "Cole", "Ashlin", "Zach", "Nathaniel"]
raceOptions = ["Solos", "Teams"]
teamOptions = ["2v2", "Relays"]
oneononeOptions = ["1v1", "1v1v1", "1v1v1v1"]
drinkingOptions = ["Yes", "No"]
firstPlace = None
secondPlace = None
thirdPlace = None
fourthPlace = None
teamMode = None
drinkingRace = None
thirdPlace = None
fourthPlace = None
rating_three = None
rating_fourth = None
change_third = None
change_fourth = None

st.subheader("Please fill out all of the fields below and then click run to update player BKR in the database")
drinkingRace = st.segmented_control(label="Was it a drinking race?", options=drinkingOptions)

modeSelection = st.selectbox(label="What type of race was it?", options=raceOptions)

if modeSelection == "Teams":
    teamMode = st.selectbox(label="What type of team race was it?", options=teamOptions, index=None)
    

else:
    onevoneSelection = st.selectbox(label="Was it a 1v1, 1v1v1, or a 1v1v1v1?", options=oneononeOptions)

    match onevoneSelection:
        case "1v1":
            col1, col2 = st.columns(2)
            with col1:
                firstPlace = st.selectbox(label="Who won the race?", options=players, index=None, key="1v1_1")
            with col2:
                secondPlace = st.selectbox(label="Who lost the race?", options=players, index=None, key="1v1_2")
                
        case "1v1v1":
            col1, col2, col3 = st.columns(3)
            with col1:
                firstPlace = st.selectbox(label="1st Place", options=players, index=None, key="1v2_1")
            with col2:
                secondPlace = st.selectbox(label="2nd Place", options=players, index=None, key="1v2_2")
            with col3:
                thirdPlace = st.selectbox(label="3rd Place", options=players, index=None, key="1v2_3")
                
        case "1v1v1v1":
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                firstPlace = st.selectbox(label="1st Place", options=players, index=None, key="1v3_1")
            with col2:
                secondPlace = st.selectbox(label="2nd Place", options=players, index=None, key="1v3_2")
            with col3:
                thirdPlace = st.selectbox(label="3rd Place", options=players, index=None, key="1v3_3")
            with col4:
                fourthPlace = st.selectbox(label="4th Place", options=players, index=None, key="1v3_4")


st.divider()

if st.button("Run Update"):
    valid_input = False
    
    if modeSelection == "Solos":
        if onevoneSelection == "1v1" and firstPlace and secondPlace:
            valid_input = True
        elif onevoneSelection == "1v1v1" and firstPlace and secondPlace and thirdPlace:
            valid_input = True
        elif onevoneSelection == "1v1v1v1" and firstPlace and secondPlace and thirdPlace and fourthPlace:
            valid_input = True
            
    elif modeSelection == "Teams" and teamMode:
        
        valid_input = True 


# 2. Execution Logic
    if valid_input:
        st.success("Inputs valid, Checking Database...")
        
        with st.spinner("Calculating..."):
            time.sleep(1)

            addUniquePlayer(firstPlace)
            playerFirstProfile = fetchPlayerData(firstPlace)

            addUniquePlayer(secondPlace)
            playerSecondProfile = fetchPlayerData(secondPlace)

            playerThirdProfile = None # Start empty to avoid errors
            if thirdPlace is not None:
                addUniquePlayer(thirdPlace)
                playerThirdProfile = fetchPlayerData(thirdPlace)

            playerFourthProfile = None # Start empty
            if fourthPlace is not None:
                addUniquePlayer(fourthPlace)
                playerFourthProfile = fetchPlayerData(fourthPlace)
#THE ELO CALCULATIONS 
        k_factor = 100

        change_first = 0
        change_second = 0
        change_third = 0
        change_fourth = 0

        rating_one = playerFirstProfile['Beerlo'] if playerFirstProfile else None
        print(rating_one)
        rating_two = playerSecondProfile['Beerlo'] if playerSecondProfile else None
        print(rating_two)
        rating_three = playerThirdProfile['Beerlo'] if playerThirdProfile else None
        print(rating_three)
        rating_fourth = playerFourthProfile['Beerlo'] if playerFourthProfile else None
        print(rating_fourth)

        change_first += k_factor * (1 - expected_result(rating_one, rating_two))
        if rating_three is not None:
            change_first += k_factor * (1 - expected_result(rating_one, rating_three))
        if rating_fourth is not None:
            change_first += k_factor * (1 - expected_result(rating_one, rating_fourth))


        change_second += k_factor * (0 - expected_result(rating_two, rating_one))
        if rating_three is not None:
            change_second += k_factor * (1 - expected_result(rating_two, rating_three))
        if rating_fourth is not None:
            change_second += k_factor * (1 - expected_result(rating_two, rating_fourth))

        if rating_three is not None:
            change_third += k_factor * (0 - expected_result(rating_three, rating_one))
            change_third += k_factor * (0 - expected_result(rating_three, rating_two))
            if rating_fourth is not None:
                change_third += k_factor * (1 - expected_result(rating_three, rating_fourth))


        if rating_fourth is not None:
            change_fourth += k_factor * (0 - expected_result(rating_fourth, rating_one))
            change_fourth += k_factor * (0 - expected_result(rating_fourth, rating_two))
            change_fourth += k_factor * (0 - expected_result(rating_fourth, rating_three))

        
        table_data = []

        table_data.append({
            "Player" : firstPlace,
            "Initial Beerlo" : rating_one,
            "Change": change_first,
            "Final Beerlo": (rating_one + change_first)
        })

        table_data.append({
            "Player" : secondPlace,
            "Initial Beerlo" : rating_two,
            "Change": change_second,
            "Final Beerlo": (rating_two + change_second)
        })
        if rating_three is not None:
            table_data.append({
                "Player" : thirdPlace,
                "Initial Beerlo" : rating_three,
                "Change": change_third,
                "Final Beerlo": (rating_three + change_third)
            })
        if rating_fourth is not None:
            table_data.append({
                "Player" : fourthPlace,
                "Initial Beerlo" : rating_fourth,
                "Change": change_fourth,
                "Final Beerlo": (rating_fourth + change_fourth)
            })


        UITable = pd.DataFrame(table_data)

        st.dataframe(UITable, use_container_width=True, hide_index=True)
        st.toast("Calculations Completed!", icon="✅")
        st.divider()
        st.warning("Make sure EVERYTHING is correct before you push changes to the database. These are hard if not impossible to reverse, I do have backups if something happens. Thanks!")
        confirmChanges = st.button("Push Changes?")
        print(confirmChanges)

        

    else:
        st.error("Missing information. Please ensure all fields for the selected mode are filled.")