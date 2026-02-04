import streamlit as st
import sqlite3
import pandas as pd
import random
import time
players = [
    "Aiden", "Alex", "Ashlin", "Brad", "Cam", "Carson", "Charlie", "Cole", 
    "Easton", "Ethan", "Ewan", "George", "Jake", "Julian", "Kaiden", 
    "Nathaniel", "Nolan", "Owen", "Rocky", "Ryley", "Santi", "Ty", "Zach"
]

modes = ["Solos", "Teams"]
st.title("Log Beerio History")

st.info("This logger is just for logging the history of beerios. Fill out all the fields and then push it to the server, if you have the dates correctly setup in the RACE HISTORY it will automatically pull how many drinks were drank and what races were done at that beerio!")

date = st.date_input("Please input the date that the Beerio was played!")

game = st.text_input("Please enter the game that was played at this Beerio")

type = st.selectbox("Please select the gamemode that was played at the Beerio", options=modes)

if type == "Teams":
    first = st.multiselect("Please select the players that got first in the Beerio", players, )
    second = st.multiselect("Please select the players that got second in the Beerio", players)
    third = st.multiselect("Please select the players that got third in the Beerio", players)
    fourth = st.multiselect("Please select the players that got fourth in the Beerio", players)
else:
        first = st.selectbox("Please select the player that got first in the Beerio", players, index = None)
        second = st.selectbox("Please select the player that got second in the Beerio", players, index = None)
        third = st.selectbox("Please select the player that got third in the Beerio", players, index = None)
        fourth = st.selectbox("Please select the player that got fourth in the Beerio", players, index = None)

playerCount = st.text_input("Please enter how many players were at the Beerio in a whole number (Ex. 15)")



if 'saved_event_id' not in st.session_state:
    st.session_state.saved_event_id = None

clean_name = game.strip().replace(" ", "_").lower()


if 'saved_event_id' not in st.session_state:
    st.session_state.saved_event_id = ""

if st.button("Format and Validate Data + Generate EventID"):

    new_id = clean_name + str(random.randint(00000, 99999))
    

    st.session_state.saved_event_id = new_id

    dataTable = pd.DataFrame([
        {"EventID": new_id, "Game": game, "Type": type, "Winner": first, "Date": date, "Total Players": playerCount}
    ])
    st.divider()
    st.dataframe(dataTable, use_container_width=True, hide_index=True)
    st.warning("EventID Created! Please proceed to push to database.")
    st.info(f"Your event id is: {new_id}", icon="🚨")


elif st.session_state.saved_event_id:
    st.info(f"Ready to push Event ID: {st.session_state.saved_event_id}", icon="✅")



if st.button("Push details to database! - Only press when you formatted the data!"):

    if not st.session_state.saved_event_id:
        st.error("Please click 'Format and Validate' first to generate an Event ID!")
    else:

        final_event_id = st.session_state.saved_event_id
        

        def format_entry(entry):
            if isinstance(entry, list):
                return ", ".join(entry)
            return entry if entry is not None else "N/A"

        p_first = format_entry(first)
        p_second = format_entry(second)
        p_third = format_entry(third)
        p_fourth = format_entry(fourth)
        p_date = str(date)

        try:
            conn = sqlite3.connect('streamlit\\databasetesting\\databasetest1.db')
            c = conn.cursor()
            
            c.execute('''
                INSERT INTO "beerio-history" (
                    "EventID", "Game", "Type", "Winner", "Second", 
                    "Third", "Fourth", "Date", "Total Players", "Drinks Consumed"
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                final_event_id, game, type, p_first, p_second, 
                p_third, p_fourth, p_date, playerCount, 0
            ))
            
            conn.commit()
            st.balloons()
            st.success(f"Successfully pushed Event {final_event_id} to database!")
            

            st.session_state.saved_event_id = ""
            
        except sqlite3.IntegrityError as e:
            st.error(f"Database Error: {e}")
            st.info("Tip: This ID might already exist.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            conn.close()