"""
Custom PyTorch Dataset class for the spectogram/music data.
"""
import os
import sys
import cv2
import torch
import pyprojroot
import numpy as np
import pandas as pd

# Make it to where paths only need to be from the repo folder.
root = pyprojroot.find_root(pyprojroot.has_dir(".git"))
sys.path.append(str(root))

# When generating the spectograms, some audio files produced black images so exclude those images.
exclude = [137, 146, 187, 206, 236, 449, 488, 621, 646, 661, 707, 1016, 1109, 1134, 1142, 1161, 1167, 1171, 1184, 1429]


class MusicDataset(torch.utils.data.Dataset):
    """
    Custom PyTorch Dataset class for the spectogram/music data.

    args:
        csv_file_path (str): path to a csv file.
        data_dir (str): directory where the data associated with the csv file is stored.
    """

    def __init__(self, csv_file_path: str, data_dir: str) -> None:
        """
        Constructor for MusicDataset class.
        """    
        # Save the location of the data (in other words, the spectograms.)
        self.data_dir = os.path.join(root, data_dir)
        self.csv = csv_file_path

        # Merge root and csv_file_path and read csv file.
        self.df = pd.read_csv(os.path.join(root, csv_file_path))

        # Remove exluded values.
        for num in exclude: self.df = self.df[self.df.song_id != num]
    

    def print_df(self) -> None:
        """
        Print the current dataframe of the data based on the given csv file.
        """
        print(f"\nCurrent dataframe based on [{self.csv}]")
        print(self.df)


    def __len__(self) -> int:
        """
        Returns the number of images in the dataset.

        Return value: int
        """
        return len(self.df)


    def __getitem__(self, idx) -> (torch.Tensor, str):
        """
        Fetches the image and corresponding label for a given index.

        Args:
            idx (int): index of the image (spectogram) to fetch

        Return value: torch.Tensor of image str of mood type.
        """
        # Get the spectogram at the given index (idx).
        row = self.df.iloc[idx]
        img_fname = row["song_id"]
        img_file_path = os.path.join(self.data_dir, f"{img_fname}.png")
        img = cv2.imread(img_file_path, cv2.IMREAD_ANYDEPTH)
        
        # Return the image and associated mood type label.
        return torch.from_numpy(img), row["mood"]


if __name__ == "__main__":
    # Data directory.
    csv_path = "data/mood.csv"
    data_dir = "data/spectograms"

    dataset = MusicDataset(csv_file_path=csv_path, data_dir=data_dir)

    print(len(dataset))
    print(dataset[0])
    dataset.print_df()
