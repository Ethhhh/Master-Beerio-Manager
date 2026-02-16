import pandas as pd

# Load the dataset
df = pd.read_csv('RaceData/racedatav2.csv')
print(df.head())
print(df.info())

def get_expected_result(rating_a, rating_b):
    """
    Calculates the expected probability of Player A beating Player B
    based on their current Elo ratings.
    """
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 4000))


