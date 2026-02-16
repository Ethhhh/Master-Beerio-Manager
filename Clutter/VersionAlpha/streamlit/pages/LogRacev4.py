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


st.logo = ("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Beer_icon.svg/1200px-Beer_icon.svg.png") # Placeholder image
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

st.subheader("Please fill out all of the fields below")


eventID = st.text_input("EventID (Optional)", help="Enter a custom ID like 'MK8_01' or leave blank.")
mapPick = st.text_input("Map Name (Optional)")
drinkingRace = st.segmented_control(label="Was it a drinking race?", options=drinkingOptions)
modeSelection = st.selectbox(label="What type of race was it?", options=raceOptions)


if modeSelection == "Teams":
    teamMode = st.selectbox(label="Team Format", options=teamOptions, index=None)
    

    if teamMode == "Relays":
        st.write("---")
        st.info("Select the 3 players for each finishing position (12 Players Total).")
        
        c1, c2, c3, c4 = st.columns(4)
        

        with c1:
            st.caption("First Place Team")
            r1_p1 = st.selectbox("P1", options=players, key="r1_1")
            r1_p2 = st.selectbox("P2", options=players, key="r1_2")
            r1_p3 = st.selectbox("P3", options=players, key="r1_3")
            

        with c2:
            st.caption("Second Place Team")
            r2_p1 = st.selectbox("P1", options=players, key="r2_1")
            r2_p2 = st.selectbox("P2", options=players, key="r2_2")
            r2_p3 = st.selectbox("P3", options=players, key="r2_3")


        with c3:
            st.caption("Third Place Team")
            r3_p1 = st.selectbox("P1", options=players, key="r3_1")
            r3_p2 = st.selectbox("P2", options=players, key="r3_2")
            r3_p3 = st.selectbox("P3", options=players, key="r3_3")


        with c4:
            st.caption("Fourth Place Team")
            r4_p1 = st.selectbox("P1", options=players, key="r4_1")
            r4_p2 = st.selectbox("P2", options=players, key="r4_2")
            r4_p3 = st.selectbox("P3", options=players, key="r4_3")


        if r1_p1 and r2_p1 and r3_p1 and r4_p1:
            firstPlace = f"{r1_p1} & {r1_p2} & {r1_p3}"
            secondPlace = f"{r2_p1} & {r2_p2} & {r2_p3}"
            thirdPlace = f"{r3_p1} & {r3_p2} & {r3_p3}"
            fourthPlace = f"{r4_p1} & {r4_p2} & {r4_p3}"


    elif teamMode == "2v2":
        st.write("---")
        st.info("Select the Winning Team and the Losing Teams players!")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Winners")
            w1 = st.selectbox("Winner #1", options=players, key="2v2_w1")
            w2 = st.selectbox("Winner #2", options=players, key="2v2_w2")
        with col2:
            st.subheader("Losers")
            l1 = st.selectbox("Loser #1", options=players, key="2v2_l1")
            l2 = st.selectbox("Loser #2", options=players, key="2v2_l2")

        if w1 and w2 and l1 and l2:
            firstPlace = w1
            secondPlace = w2
            thirdPlace = l1
            fourthPlace = l2


else:
    onevoneSelection = st.selectbox(label="Was it a 1v1, 1v1v1, or a 1v1v1v1?", options=oneononeOptions)
    if onevoneSelection == "1v1":
        col1, col2 = st.columns(2)
        with col1: firstPlace = st.selectbox("Winner", players, key="1v1_1")
        with col2: secondPlace = st.selectbox("Loser", players, key="1v1_2")
    elif onevoneSelection == "1v1v1":
        col1, col2, col3 = st.columns(3)
        with col1: firstPlace = st.selectbox("1st", players, key="1v2_1")
        with col2: secondPlace = st.selectbox("2nd", players, key="1v2_2")
        with col3: thirdPlace = st.selectbox("3rd", players, key="1v2_3")
    elif onevoneSelection == "1v1v1v1":
        c1, c2, c3, c4 = st.columns(4)
        with c1: firstPlace = st.selectbox("1st", players, key="1v3_1")
        with c2: secondPlace = st.selectbox("2nd", players, key="1v3_2")
        with c3: thirdPlace = st.selectbox("3rd", players, key="1v3_3")
        with c4: fourthPlace = st.selectbox("4th", players, key="1v3_4")

st.divider()


if 'calculation_results' not in st.session_state:
    st.session_state.calculation_results = None

if st.button("Run Calculations!"):

    valid_input = False
    if modeSelection == "Solos" and firstPlace and secondPlace: valid_input = True
    elif modeSelection == "Teams" and teamMode: valid_input = True

    if valid_input:
        st.success("Valid inputs, running math...")
        with st.spinner("Crunching numbers..."):
            time.sleep(0.5)
            

            if modeSelection == "Teams" and teamMode == "Relays":
                
                def get_team_stats(names):
                    stats = []
                    total_elo = 0
                    for name in names:
                        if name is None: st.error("Missing player!"); st.stop()
                        addUniquePlayer(name)
                        data = fetchPlayerData(name)
                        if data is None: st.error(f"Error finding {name}"); st.stop()
                        stats.append(data)
                        total_elo += data['Beerlo']
                    return stats, total_elo / 3

                t1_stats, t1_avg = get_team_stats([r1_p1, r1_p2, r1_p3])
                t2_stats, t2_avg = get_team_stats([r2_p1, r2_p2, r2_p3])
                t3_stats, t3_avg = get_team_stats([r3_p1, r3_p2, r3_p3])
                t4_stats, t4_avg = get_team_stats([r4_p1, r4_p2, r4_p3])

                k_factor = 100
                
   
                c1 = k_factor * ((1 - expected_result(t1_avg, t2_avg)) + (1 - expected_result(t1_avg, t3_avg)) + (1 - expected_result(t1_avg, t4_avg)))
                c2 = k_factor * ((0 - expected_result(t2_avg, t1_avg)) + (1 - expected_result(t2_avg, t3_avg)) + (1 - expected_result(t2_avg, t4_avg)))
                c3 = k_factor * ((0 - expected_result(t3_avg, t1_avg)) + (0 - expected_result(t3_avg, t2_avg)) + (1 - expected_result(t3_avg, t4_avg)))
                c4 = k_factor * ((0 - expected_result(t4_avg, t1_avg)) + (0 - expected_result(t4_avg, t2_avg)) + (0 - expected_result(t4_avg, t3_avg)))


                table_data = []
                for p in t1_stats: table_data.append({"Player": p['Name'], "Initial Beerlo": p['Beerlo'], "Change": c1, "Final Beerlo": p['Beerlo'] + c1})
                for p in t2_stats: table_data.append({"Player": p['Name'], "Initial Beerlo": p['Beerlo'], "Change": c2, "Final Beerlo": p['Beerlo'] + c2})
                for p in t3_stats: table_data.append({"Player": p['Name'], "Initial Beerlo": p['Beerlo'], "Change": c3, "Final Beerlo": p['Beerlo'] + c3})
                for p in t4_stats: table_data.append({"Player": p['Name'], "Initial Beerlo": p['Beerlo'], "Change": c4, "Final Beerlo": p['Beerlo'] + c4})
                
                st.session_state.calculation_results = table_data


            elif modeSelection == "Teams" and teamMode == "2v2":
                addUniquePlayer(firstPlace); p1 = fetchPlayerData(firstPlace)
                addUniquePlayer(secondPlace); p2 = fetchPlayerData(secondPlace)
                addUniquePlayer(thirdPlace); p3 = fetchPlayerData(thirdPlace)
                addUniquePlayer(fourthPlace); p4 = fetchPlayerData(fourthPlace)

                avg_win = (p1['Beerlo'] + p2['Beerlo']) / 2
                avg_loss = (p3['Beerlo'] + p4['Beerlo']) / 2
                
                k_factor = 100
                change = k_factor * (1 - expected_result(avg_win, avg_loss))


                table_data = []
                for p in [p1, p2]: 
                    table_data.append({"Player": p['Name'], "Initial Beerlo": p['Beerlo'], "Change": change, "Final Beerlo": p['Beerlo'] + change})
                for p in [p3, p4]: 
                    table_data.append({"Player": p['Name'], "Initial Beerlo": p['Beerlo'], "Change": -change, "Final Beerlo": p['Beerlo'] - change})
                
                st.session_state.calculation_results = table_data


            else:
                addUniquePlayer(firstPlace)
                playerFirstProfile = fetchPlayerData(firstPlace)
                addUniquePlayer(secondPlace)
                playerSecondProfile = fetchPlayerData(secondPlace)
                
                rating_one = playerFirstProfile['Beerlo']
                rating_two = playerSecondProfile['Beerlo']
                
                rating_three = None
                if thirdPlace: 
                    addUniquePlayer(thirdPlace)
                    p3 = fetchPlayerData(thirdPlace)
                    rating_three = p3['Beerlo']
                    
                rating_fourth = None
                if fourthPlace: 
                    addUniquePlayer(fourthPlace)
                    p4 = fetchPlayerData(fourthPlace)
                    rating_fourth = p4['Beerlo']

                k_factor = 100
                change_first = k_factor * (1 - expected_result(rating_one, rating_two))
                if rating_three: change_first += k_factor * (1 - expected_result(rating_one, rating_three))
                if rating_fourth: change_first += k_factor * (1 - expected_result(rating_one, rating_fourth))
                
                change_second = k_factor * (0 - expected_result(rating_two, rating_one))
                if rating_three: change_second += k_factor * (1 - expected_result(rating_two, rating_three))
                if rating_fourth: change_second += k_factor * (1 - expected_result(rating_two, rating_fourth))

                change_third = 0
                if rating_three:
                    change_third += k_factor * (0 - expected_result(rating_three, rating_one))
                    change_third += k_factor * (0 - expected_result(rating_three, rating_two))
                    if rating_fourth: change_third += k_factor * (1 - expected_result(rating_three, rating_fourth))

                change_fourth = 0
                if rating_fourth:
                    change_fourth += k_factor * (0 - expected_result(rating_fourth, rating_one))
                    change_fourth += k_factor * (0 - expected_result(rating_fourth, rating_two))
                    change_fourth += k_factor * (0 - expected_result(rating_fourth, rating_three))


                table_data = []
                table_data.append({"Player": firstPlace, "Initial Beerlo": rating_one, "Change": change_first, "Final Beerlo": rating_one + change_first})
                table_data.append({"Player": secondPlace, "Initial Beerlo": rating_two, "Change": change_second, "Final Beerlo": rating_two + change_second})
                if rating_three: table_data.append({"Player": thirdPlace, "Initial Beerlo": rating_three, "Change": change_third, "Final Beerlo": rating_three + change_third})
                if rating_fourth: table_data.append({"Player": fourthPlace, "Initial Beerlo": rating_fourth, "Change": change_fourth, "Final Beerlo": rating_fourth + change_fourth})

                st.session_state.calculation_results = table_data
    else:
        st.error("Missing fields. Please check all inputs.")


if st.session_state.calculation_results is not None:

    UITable = pd.DataFrame(st.session_state.calculation_results)
    
    st.dataframe(
        UITable, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Initial Beerlo": st.column_config.NumberColumn(format="%d"), # Display as Integer
            "Change": st.column_config.NumberColumn(format="%+d"),        # Display as +10 / -10
            "Final Beerlo": st.column_config.NumberColumn(format="%d")    # Display as Integer
        }
    )
    st.divider()
    st.warning("Make sure EVERYTHING is correct before pushing!")

    with st.expander("📅 Backfill / Manual Date (Click to open)"):
        st.caption("Use this only if you are uploading old data.")
        is_backfill = st.checkbox("Manually set date and time?", key="backfill_main")
        
        if is_backfill:
            col_d, col_t = st.columns(2)
            with col_d: manual_date = st.date_input("Date")
            with col_t: manual_time = st.time_input("Time", value=datetime.time(12, 00))
        else:
            st.info("Using current Date & Time.")


    if st.button("Push Changes?"):
        try:
            with sqlite.connect("streamlit\\databasetesting\\databasetest1.db") as conn:
                cursor = conn.cursor()

                import datetime
                if is_backfill:
                    final_timestamp = datetime.datetime.combine(manual_date, manual_time).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    final_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                for row in st.session_state.calculation_results:
                    cursor.execute("UPDATE players SET Beerlo = ?, Races_Done = Races_Done + 1 WHERE Name = ?", (row["Final Beerlo"], row["Player"]))
                    if drinkingRace == "Yes":
                        cursor.execute("UPDATE players SET Drinking_Races = Drinking_Races + 1 WHERE Name = ?", (row["Player"],))


                final_race_type = teamMode if modeSelection == "Teams" else onevoneSelection
                cursor.execute(
                    """INSERT INTO "race-history" (EventID, "Race Type", Winner, Second, Third, Fourth, Map) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (eventID if eventID else None, final_race_type, firstPlace, secondPlace, thirdPlace, fourthPlace, mapPick)
                )
                new_race_id = cursor.lastrowid

                for row in st.session_state.calculation_results:
                    cursor.execute(
                        """INSERT INTO elo_history (RaceID, Name, StartingElo, Change, FinalElo, Date) VALUES (?, ?, ?, ?, ?, ?)""",
                        (new_race_id, row["Player"], row["Initial Beerlo"], row["Change"], row["Final Beerlo"], final_timestamp)
                    )

                conn.commit()
            
            st.success(f"Saved! Date: {final_timestamp}")
            st.balloons()
            with st.empty():
                for i in range(3, 0, -1):
                    st.write(f"Refreshing in {i}...")
                    time.sleep(1)
            st.session_state.clear()
            st.rerun()

        except Exception as e:
            st.error(f"Database Error: {e}")