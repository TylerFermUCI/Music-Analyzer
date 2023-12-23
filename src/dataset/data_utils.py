"""
Functions for working with the data.
"""

import os
import csv
import sys
import pyprojroot
import pandas as pd

# Make it to where paths only need to be from the repo folder.
root = pyprojroot.find_root(pyprojroot.has_dir(".git"))
sys.path.append(str(root))


def create_csv(data_path: str, new_file_path: str) -> None:
    """
    With input from the user, create a csv file to store metadata on data from data_path.
    Specifically, this function is used to create a csv file to store the labels for the dataset.

    Arguments:
        data_path (str): path to where the data is located.
        new_file_name (str): what to call the new csv file (inclduing the path to that file).

    Return value: None
    """
    # Merge data_path with root.
    data_path = os.path.join(root, data_path)
    
    # Check if path exists.
    if os.path.exists(data_path):
        # Create a new file.
        with open(os.path.join(root, new_file_path), 'w', newline='') as file:
            writer = csv.writer(file)
            field = ["song_id", "mood", "valence", "arousal"]
            writer.writerow(field)

            # Open the data into a dataframe.
            df = pd.read_csv(data_path)

            # Go through each song and determine it's moode based on valence and arousal.
            for i in range(len(df)):
                valence = df.iloc[i, 1]
                arousal = df.iloc[i, 3]
                if valence >= 5:
                    if arousal < 5: mood = "calm"
                    else: mood = "happy"
                else:
                    if arousal < 5: mood = "sad"
                    else: mood = "tense"
                # Write the information into the new csv file.
                difference = abs(valence - arousal)
                writer.writerow([df.iloc[i, 0], mood, valence, arousal])

    # If it doesn't, don't do anything.
    else:
        print("File doesn't exist") 
    

def create_csv_with_inputs(data_path: str, new_file_path: str) -> None:
    """
    Manually assign mood values to songs in the data_path.
    Useful if you want to assign mood values to the song yourself.

    Arguments:
        data_path (str): path to where the data is located.
        new_file_name (str): what to call the new csv file (inclduing the path to that file).

    Return value: None
    """
    # Merge data_path with root.
    data_path = os.path.join(root, data_path)
    
    # Check if path exists.
    if os.path.exists(data_path):
        # Create a new file.
        with open(os.path.join(root, new_file_path), 'w', newline='') as file:
            writer = csv.writer(file)
            field = ["song_id", "mood"]
            writer.writerow(field)

            # Open the data into a dataframe.
            df = pd.read_csv(data_path)

            # Go through each song and determine it's moode based on valence and arousal.
            for i in range(len(df)):
                song_id = df.iloc[i, 0]
                user_input = input(f"Mood of song {song_id}: ")
                if user_input.lower() == "h": mood = "happy"
                elif user_input.lower() == "e": mood = "energetic"
                elif user_input.lower() == "s": mood = "sad"
                elif user_input.lower() == "c": mood = "calm"
                else: mood = "none"
                writer.writerow([df.iloc[i, 0], mood])

    # If it doesn't, don't do anything.
    else:
        print("File doesn't exist") 


def display_csv(csv_file_path: str) -> None:
    """
    Display the contents of a csv file.

    Arguments:
        csv_file_path (str): Path to the csv file.

    Return value: None
    """
    # Merge csv_file_path with root.
    new_file_path = os.path.join(root, csv_file_path)
    
    # Check if path exists.
    if os.path.exists(new_file_path):
        # Open the data into a dataframe.
        df = pd.read_csv(new_file_path)
        print(df)

    # If it doesn't, don't do anything.
    else:
        print("File doesn't exist") 


def csv_stats(csv_file_path: str) -> None:
    """
    Print various stats about the csv_file provided (assuming that the file has the headers required).

    Required headers:
        song_id, mood, valence, arousal
    
    Arguments:
        csv_file_path (str): Path to the csv file.
    
    Return value: None
    """
    # Merge csv_file_path with root.
    new_file_path = os.path.join(root, csv_file_path)
    
    # Check if path exists.
    if os.path.exists(new_file_path):
        # Open the data into a dataframe.
        df = pd.read_csv(new_file_path)
        
        # Check for the right header.
        if df.columns.values.tolist() == ['song_id', 'mood', 'valence', 'arousal']:
            # Seperate data frame by mood.
            df_mood = df.groupby('mood')

            # Print stats about groupings.
            print("\nData Stats:")
            print(f"There are {len(df_mood.get_group('happy'))} happy songs.")
            print(f"There are {len(df_mood.get_group('sad'))} sad songs.")
            print(f"There are {len(df_mood.get_group('tense'))} tense songs.")
            print(f"There are {len(df_mood.get_group('calm'))} calm songs.\n")
        # Incorrect csv file.
        else:
            print(f"CSV file given [{csv_file_path}] does not have all the required headers of ['song_id', 'mood', 'valence', 'arousal'].")
    # If it doesn't, don't do anything.
    else:
        print("File doesn't exist")

if __name__ == "__main__":
    csv_path = "data/DEAM_Annotations/annotations averaged per song/song_level/static_annotations_averaged_songs_1_2000.csv"
    new_csv_path = "data/mood.csv"
    # display_csv(csv_path)
    # create_csv(csv_path, new_csv_path)
    csv_stats(new_csv_path)