"""
Functions for working with the data.
"""

import csv




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







if __name__ == "__main__":
    print("hello")