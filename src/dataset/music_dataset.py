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
from pytorch_lightning.utilities.types import EVAL_DATALOADERS, TRAIN_DATALOADERS

# Make it to where paths only need to be from the repo folder.
root = pyprojroot.find_root(pyprojroot.has_dir(".git"))
sys.path.append(str(root))


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
        
        # One-hot encode the mood for classification.
        self.df = pd.get_dummies(self.df, columns=["mood"])
    

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


    def __getitem__(self, idx) -> (torch.Tensor, torch.Tensor):
        """
        Fetches the image and corresponding one-hot encoded label for a given index.

        Args:
            idx (int): index of the image (spectogram) to fetch

        Return value: torch.Tensor of image and torch.Tensor of one-hot encoded label.
        """
        # Get the spectogram at the given index (idx).
        row = self.df.iloc[idx]
        img_fname = row["song_id"]
        img_file_path = os.path.join(self.data_dir, f"{img_fname}.png")
        img = cv2.imread(img_file_path, cv2.IMREAD_ANYDEPTH)

        # Fetch one hot encoded labels for all classes of mood type as a Series.
        mood_type_tensor = row[['mood_calm', 'mood_happy', 'mood_sad', 'mood_tense']]

        # Convert Series to numpy array.
        mood_type_tensor = mood_type_tensor.to_numpy().astype(np.bool_)
        
        # Convert One Hot Encoded labels to tensor.
        mood_type_tensor = torch.from_numpy(mood_type_tensor)
        
        # Convert tensor data type to Float.
        mood_type_tensor = mood_type_tensor.type(torch.FloatTensor)
        
        # Return the image and associated one-hot encoded label.
        return torch.from_numpy(img), mood_type_tensor


if __name__ == "__main__":
    # Data directory.
    csv_path = "data/mood.csv"
    data_dir = "data/spectograms"

    # Testing with BPSMouseDataset from tests.
    dataset = MusicDataset(csv_file_path=csv_path, data_dir=data_dir)

    print(dataset.__len__())
    print(dataset.__getitem__(0))
    dataset.print_df()
