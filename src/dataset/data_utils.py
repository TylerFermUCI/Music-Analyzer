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


# TODO: Finish creation of the csv file.
def create_csv(data_path: str, new_file_name: str) -> None:
    """
    With input from the user, create a csv file to store metadata on data from data_path.

    Arguments:
        data_path (str): path to where the data is located.
        new_file_name (str): what to call the new csv file.

    Return value: None
    """
    # Create a new file.
    with open(f'{new_file_name}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["song_title", "mood"]
        
        writer.writerow(field)
        writer.writerow(["Oladele Damilola", "40", "Nigeria"])
        writer.writerow(["Alina Hricko", "23", "Ukraine"])
        writer.writerow(["Isabel Walter", "50", "United Kingdom"])


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



if __name__ == "__main__":
    csv_path = "data/DEAM_Annotations/annotations averaged per song/song_level/static_annotations_averaged_songs_1_2000.csv"
    display_csv(csv_path)