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

# When generating the spectograms, some audio files produced black images so exclude those images.
exclude = [137, 146, 187, 206, 236, 449, 488, 621, 646, 661, 707, 1016, 1109, 1134, 1142, 1161, 1167, 1171, 1184, 1429]


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
                writer.writerow([df.iloc[i, 0], mood, valence, arousal])

    # If it doesn't, don't do anything.
    else:
        print(f"Data path [{data_path}] doesn't exist") 
    

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
        print(f"Data path [{data_path}] doesn't exist") 


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

        # Remove exluded values.
        for num in exclude: df = df[df.song_id != num]
        print(df)

    # If it doesn't, don't do anything.
    else:
        print(f"File [{new_file_path}] doesn't exist") 


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
            # Remove exluded values.
            for num in exclude: df = df[df.song_id != num]
            
            # Seperate data frame by mood.
            df_mood = df.groupby('mood')

            # Print stats about groupings.
            print("\nData Stats:")
            print(f"There are {len(df_mood.get_group('happy'))} happy songs.")
            print(f"There are {len(df_mood.get_group('sad'))} sad songs.")
            print(f"There are {len(df_mood.get_group('tense'))} tense songs.")
            print(f"There are {len(df_mood.get_group('calm'))} calm songs.")
            print(f"There are a total of {len(df)} songs.\n")
            print(f"Number of songs excluded: {len(exclude)}")
        # Incorrect csv file.
        else:
            print(f"CSV file given [{csv_file_path}] does not have all the required headers of ['song_id', 'mood', 'valence', 'arousal'].")
    # If it doesn't, don't do anything.
    else:
        print(f"File [{new_file_path}] doesn't exist")


    
def train_val_split(csv_file_path: str):
    """
    Create csv files that seperates images into training set and validation set.
    
    Arguments:
        csv_file_path (str): path to the csv file that contains all images and associated labels.
    
    Return value: None
    """
    # Merge csv_file_path with root.
    new_file_path = os.path.join(root, csv_file_path)
    
    # Check if path exists.
    if os.path.exists(new_file_path):
        # Open the data into a dataframe.
        df = pd.read_csv(new_file_path)

        # Remove exluded values.
        for num in exclude: df = df[df.song_id != num]

        # Seperate df by mood type.
        happy_df = df[df.mood == "happy"]
        sad_df = df[df.mood == "sad"]
        calm_df = df[df.mood == "calm"]
        tense_df = df[df.mood == "tense"]
        
        sampled_happy = happy_df.sample(n=200)
        extra_happy = happy_df[~happy_df.apply(tuple,1).isin(sampled_happy.apply(tuple,1))]

        sampled_sad = sad_df.sample(n=200)
        extra_sad = sad_df[~sad_df.apply(tuple,1).isin(sampled_sad.apply(tuple,1))]

        sampled_calm = calm_df.sample(n=200)
        extra_calm = calm_df[~calm_df.apply(tuple,1).isin(sampled_calm.apply(tuple,1))]
        
        sampled_tense = tense_df.sample(n=200)
        extra_tense = tense_df[~tense_df.apply(tuple,1).isin(sampled_tense.apply(tuple,1))]
        
        # Establish base path.
        base_path = os.path.split(new_file_path)[0]
        
        # Combine sampled dataframes for training.
        training_frames = [sampled_happy, sampled_sad, sampled_calm, sampled_tense]
        sampled_combined = pd.concat(training_frames).sort_values("song_id")
        
        # Create training set csv file.  
        training_csv_path = os.path.join(base_path, "mood_training.csv")
        sampled_combined.to_csv(training_csv_path, index=False)
        print(f"Created training csv file at [{training_csv_path}]")

        # Get samples of validation data from the extra songs not included in training.
        min_n = min(len(extra_happy), len(extra_calm), len(extra_sad), len(extra_tense))
        val_happy = extra_happy.sample(n=min_n)
        val_sad = extra_sad.sample(n=min_n)
        val_calm = extra_calm.sample(n=min_n)
        val_tense = extra_tense.sample(n=min_n)
        
        # Combine sampled dataframes for validation.
        val_frames = [val_calm, val_happy, val_sad, val_tense]
        val_combined = pd.concat(val_frames).sort_values("song_id")

        # Create validation set csv file.  
        val_csv_path = os.path.join(base_path, "mood_validation.csv")
        val_combined.to_csv(val_csv_path, index=False)
        print(f"Created validation csv file at [{val_csv_path}]")
    # If it doesn't, don't do anything.
    else:
        print(f"File [{new_file_path}] doesn't exist")

if __name__ == "__main__":
    csv_path = "data/DEAM_Annotations/annotations averaged per song/song_level/static_annotations_averaged_songs_1_2000.csv"
    new_csv_path = "data/mood.csv"
    # display_csv(csv_path)
    # create_csv(csv_path, new_csv_path)
    # csv_stats(new_csv_path)
    train_val_split(new_csv_path)
