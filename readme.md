WELCOME TO THE MUTHAFUCKIN REPO

(IMPORTANT) https://python-fiddle.com/saved/33cce59b-2158-44af-94ab-f3d35289d02e -- This link allows you to run the Elo simulator in a webpage, simply click run and scroll to the bottom to see the output, you can change the values as you see fit (IMPORANT)

################# - What Changing Each Value Affects - #################

STARTING_ELO = 10000.0 # this is the elo that every player will start at 

K_FACTOR = 250.0 # this is the volatility in a race. Basically the max amount of points that can change. Keep in mind that when you win in first you are technically winning three races(AvB, AvC, AvD) so technically you could win up to 750 points, this is very rare, if not impossible though and usually the max discrepancy is about 100+- points.

There is one protection for second place, if they are losing points (1:Cole 2:Cam 3:Kaiden 4:Alex) then the amount of points they are losing is cut in half (there were some HUGE upsets so this is personal preference)

DIVIDER = 1200.0  - the amount of possible spread between ranks

TOTAL_RACES = 200 (the longer the sim the more possible spread but the max at a div level of 1200 will be about 5-6 thousand

If you know how python works then this should be pretty easy to test the code, if not good luck

Feel free to check the "VersionAlpha" folder this contains everything that was in the original test versions of the calculator

The simulator folder has my more refinded system for the elo calculator so you can simulate a ton of races in there if youd like.

Extra and planning arent really that important but feel free to look if you are curious as to how I built some of the chings in here 

If you go to the streamlit folder and download streamlit (pip install streamlit) and then execute any of the four .py files that are in the streamlit folder (python -m streamlit run streamlit\logracev3.py), you can see what the planned UI was going to look like, but that is defintly not set in stone and for all I know might completely change in the future. 

If you are curious about how the SQL databases may be laid out check out the databasetesting in the streamlit folder. You can use (https://sqlitebrowser.org/) to view the database.

BUT THE MAIN THING RIGHT NOW IS THE SIM, FUCK AROUND WITH THE NUMBERS AND TELL ME WHAT YOU FIND FIT! - You can change any of the settings around the top of the code, and any of the player skill ratings if youd like, or if your so inclined you can try changing the straight up code around too.

good luck jesowen

Use visual studio code (https://code.visualstudio.com/) to view and test the simulator, MAKE SURE THE PYTHON extension is installed.
