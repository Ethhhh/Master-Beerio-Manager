#packages
import streamlit as st
import pandas as pd
import sqlite3 as sql
import math
#page setup
st.logo=("")

#lists
players = ["Cam", "Nolan", "Owen", "Julian", "Ethan", "Kaiden", "Jake", "Alex", "Aiden", "Easton", "Charlie", "Ryley", "Rocky", "Ty", "Santi", "Ewan", "Carson", "George", "Brad", "Cole", "Ashlin", "Zach", "Nathaniel"]
raceOptions = ["Solos", "Teams"]
teamOptions = ["2v2", "Relays"]
oneononeOptions = ["1v1", "1v1v1", "1v1v1v1"]

#functions 
#code
st.title("Log Races")

st.badge("Testing", color="yellow")

st.subheader("Please fill out all of the fields below and then click run to update player BKR in the database")

modeSelection = st.selectbox(label="What type of race was it?", options=raceOptions)

if modeSelection == "Teams":
    teamMode = st.selectbox(label="What type of team race was it?", options= teamOptions, index = None)

else:
  onevoneSelection = st.selectbox(label="Was it a 1v1, 1v1v1, or a 1v1v1v1?", options=oneononeOptions)

  match onevoneSelection:
     case "1v1":
        firstPlace = st.selectbox(label="Who won the race?", options=players, index = None)
        secondPlace = st.selectbox(label="Who lost the race?", options=players, index = None)
     case "1v1v1":
        print("1v1v1")
     case "1v1v1v1":
        print("1v1v1v1")
