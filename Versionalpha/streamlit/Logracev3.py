import streamlit as st
import pandas as pd
import sqlite3 as sqlite
import math
import datetime
import time

connection = sqlite.connect("streamlit\\databasetesting\\databasetest1.db")
cursor = connection.cursor()


def addUniquePlayer(player_name):
    try:
        with sqlite.connect("streamlit\\databasetesting\\databasetest1.db") as conn:
            cursor = conn.cursor()
            # The database engine handles the check for us now
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

        # Check result
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

# --- Page Setup ---
st.logo = ("") 
st.title("Log Races")
st.badge("Testing", color="yellow")


players = [
    "Aiden", "Alex", "Ashlin", "Brad", "Cam", "Carson", "Charlie", "Cole", 
    "Easton", "Ethan", "Ewan", "George", "Jake", "Julian", "Kaiden", 
    "Nathaniel", "Nolan", "Owen", "Rocky", "Ryley", "Santi", "Ty", "Zach"
]
raceOptions = ["Solos", "Teams"]
teamOptions = ["2v2", "Relays"]
oneononeOptions = ["1v1", "1v1v1", "1v1v1v1"]
drinkingOptions = ["Yes", "No"]

# Initialize variables
firstPlace = None
secondPlace = None
thirdPlace = None
fourthPlace = None
teamMode = None
rating_three = None
rating_fourth = None
change_third = None
change_fourth = None

st.subheader("Please fill out all of the fields below and then click run to update player BKR in the database")

eventID = st.text_input("Please enter a EventID you created for this Beerio (optional but highly recommended)")

mapPick = st.text_input("Please enter the name of the map that you played on (optional nut recommended)")

drinkingRace = st.segmented_control(label="Was it a drinking race?", options=drinkingOptions)

modeSelection = st.selectbox(label="What type of race was it?", options=raceOptions)

if modeSelection == "Teams":
    teamMode = st.selectbox(label="What type of team race was it?", options=teamOptions, index=None)

    if teamMode == "Relays":
        print()

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

if 'calculation_results' not in st.session_state:
    st.session_state.calculation_results = None

if st.button("Run Calculations!"):
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
        
        with st.spinner("Calculating... ya fool"):
            time.sleep(1)

            addUniquePlayer(firstPlace)
            playerFirstProfile = fetchPlayerData(firstPlace)

            addUniquePlayer(secondPlace)
            playerSecondProfile = fetchPlayerData(secondPlace)

            playerThirdProfile = None 
            if thirdPlace is not None:
                addUniquePlayer(thirdPlace)
                playerThirdProfile = fetchPlayerData(thirdPlace)

            playerFourthProfile = None 
            if fourthPlace is not None:
                addUniquePlayer(fourthPlace)
                playerFourthProfile = fetchPlayerData(fourthPlace)


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

        # --- ROUNDING LOGIC APPLIED HERE ---
        # I wrapped the values in int(round(...)) to make them whole numbers
        
        table_data.append({
            "Player" : firstPlace,
            "Initial Beerlo" : rating_one,
            "Change": int(round(change_first)),
            "Final Beerlo": int(round(rating_one + change_first))
        })

        table_data.append({
            "Player" : secondPlace,
            "Initial Beerlo" : rating_two,
            "Change": int(round(change_second)),
            "Final Beerlo": int(round(rating_two + change_second))
        })
        if rating_three is not None:
            table_data.append({
                "Player" : thirdPlace,
                "Initial Beerlo" : rating_three,
                "Change": int(round(change_third)),
                "Final Beerlo": int(round(rating_three + change_third))
            })
        if rating_fourth is not None:
            table_data.append({
                "Player" : fourthPlace,
                "Initial Beerlo" : rating_fourth,
                "Change": int(round(change_fourth)),
                "Final Beerlo": int(round(rating_fourth + change_fourth))
            })


        st.session_state.calculation_results = table_data

    else:
        st.error("Missing information. Please ensure all fields for the selected mode are filled.")


if st.session_state.calculation_results is not None:
    

    UITable = pd.DataFrame(st.session_state.calculation_results)
    st.dataframe(UITable, use_container_width=True, hide_index=True)
    st.toast("Calculations Completed!", icon="✅")
    
    st.divider()
    st.warning("Make sure EVERYTHING is correct before you push changes to the database. These are hard if not impossible to reverse, I do have backups if something happens. Thanks!💖")


    # (Placed INSIDE the check so it only shows when you have data to push)
    with st.expander("📅 Backfill / Manual Date (Click to open)"):
        st.caption("Use this only if you are uploading old data. Leave unchecked for live races.")
        is_backfill = st.checkbox("Manually set date and time?", key="backfill_check_unique")
        
        if is_backfill:
            col_d, col_t = st.columns(2)
            with col_d:
                manual_date = st.date_input("Date of Race")
            with col_t:
                manual_time = st.time_input("Time of Race", value=datetime.time(12, 00))
        else:
            st.info("System will use current Date & Time automatically.")


    if st.button("Push Changes?"):
        
        # Safety Check: ensure we actually have data to push
        if st.session_state.calculation_results is None:
            st.error("No calculations found. Please run calculations first!")
            st.stop()

        try:
            with sqlite.connect("streamlit\\databasetesting\\databasetest1.db") as conn:
                cursor = conn.cursor()

                if is_backfill:

                    combined_dt = datetime.datetime.combine(manual_date, manual_time)
                    final_timestamp = combined_dt.strftime("%Y-%m-%d %H:%M:%S")
                else:

                    final_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                for row in st.session_state.calculation_results:
                    cursor.execute(
                        "UPDATE players SET Beerlo = ?, Races_Done = Races_Done + 1 WHERE Name = ?",
                        (row["Final Beerlo"], row["Player"])
                    )
                    if drinkingRace == "Yes":
                            cursor.execute(
                            "UPDATE players SET Drinking_Races = Drinking_Races + 1 WHERE Name = ?", 
                            (row["Player"],)
                        )
                

                final_race_type = teamMode if modeSelection == "Teams" else onevoneSelection

                cursor.execute(
                    """
                    INSERT INTO "race-history" 
                    (EventID, "Race Type", Winner, Second, Third, Fourth, Map) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        eventID if eventID else None,
                        final_race_type, 
                        firstPlace, 
                        secondPlace, 
                        thirdPlace, 
                        fourthPlace, 
                        mapPick
                    )
                )
                
                new_race_id = cursor.lastrowid

  
                for row in st.session_state.calculation_results:
                    cursor.execute(
                        """
                        INSERT INTO elo_history 
                        (RaceID, Name, StartingElo, Change, FinalElo, Date)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            new_race_id,
                            row["Player"],
                            row["Initial Beerlo"],
                            row["Change"],
                            row["Final Beerlo"],
                            final_timestamp
                        )
                    )

                conn.commit()
                
            st.success(f"Changes Pushed! Recorded date: {final_timestamp}")
            st.balloons()
            
            with st.empty():
                for seconds in range(5, 0, -1):
                    st.write(f"Refreshing page in {seconds} seconds...")
                    time.sleep(1)
            
            st.session_state.clear()
            st.rerun()
            
        except Exception as e:
            st.error(f"Error updating database: {e}")
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
