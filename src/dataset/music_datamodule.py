"""
For detail on the PyTorch Lightning LightningDataModule class, see the documentation:
https://lightning.ai/docs/pytorch/stable/data/datamodule.html#using-a-datamodule
"""
import os
import sys
import pyprojroot
import pytorch_lightning as pl
from torch.utils.data import DataLoader
from pytorch_lightning.utilities.types import EVAL_DATALOADERS, TRAIN_DATALOADERS

from music_dataset import MusicDataset

# Make it to where paths only need to be from the repo folder.
root = pyprojroot.find_root(pyprojroot.has_dir(".git"))
sys.path.append(str(root))

 
class MusicDataModule(pl.LightningDataModule):
    def __init__(self,
                 train_csv_file: str,
                 train_dir: str,
                 val_csv_file: str,
                 val_dir: str,
                 test_csv_file: str,
                 test_dir: str,
                 batch_size: int = 4,
                 num_workers: int = 1):
        """
        PyTorch Lightning Data Module for setting up training, testing, and validation datasets/dataloaders.

        Args:
            train_csv_file (str): The name of the csv file containing the training data.
            train_dir (str): The directory where the training data is stored.
            val_csv_file (str): The name of the csv file containing the validation data.
            val_dir (str): The directory where the validation data is stored.
            test_csv_file (str): The name of the csv file containing the test data.
            test_dir (str): The directory where the test data is stored.
            batch_size (int): The batch size to use for the DataLoader.
            num_workers (int): The number of workers to use for the DataLoader.
        """
        super().__init__()
        self.train_csv = os.path.join(root, train_csv_file)
        self.train_dir = os.path.join(root, train_dir)
        self.val_csv = os.path.join(root, val_csv_file)
        self.val_dir = os.path.join(root, val_dir)
        self.test_csv = os.path.join(root, test_csv_file)
        self.test_dir = os.path.join(root, test_dir)
        self.batch_size = batch_size
        self.num_workers = num_workers
    
        
    def setup(self, stage: str) -> None:
        """
        Assign train/val/test datasets for use in dataloaders.
        """
        if stage == "train":
            # Create the MusicDataset object for the training data.
            self.train_MusicDataset = MusicDataset(csv_file_path = self.train_csv,
                                                        data_dir = self.train_dir)

        if stage == "validate":
            # Create the MusicDataset object for the validation data.
            self.validate_MusicDataset = MusicDataset(csv_file_path = self.val_csv,
                                                            data_dir = self.val_dir)
            
        if stage == "test":
            # Create the MusicDataset object for the test data.
            self.test_MusicDataset = MusicDataset(csv_file_path = self.test_csv,
                                                        data_dir = self.test_dir)


    def train_dataloader(self) -> TRAIN_DATALOADERS:
        """
        Returns the training dataloader.
        """
        return DataLoader(self.train_MusicDataset, batch_size=self.batch_size, num_workers=self.num_workers)
    

    def val_dataloader(self) -> EVAL_DATALOADERS:
        """
        Returns the validation dataloader.
        """
        return DataLoader(self.validate_MusicDataset, batch_size=self.batch_size, num_workers=self.num_workers)
    

    def test_dataloader(self) -> EVAL_DATALOADERS:
        """
        Returns the test dataloader.
        """
        return DataLoader(self.test_MusicDataset, batch_size=self.batch_size, num_workers=self.num_workers)


if __name__ == "__main__":
    # Create Paths (without root) to specific locations. 
    train_csv_file = "data/mood_training.csv"
    train_dir = "data/spectograms"
    
    validation_csv_file = "data/mood_validation.csv"
    validation_dir = "data/spectograms"
    
    test_csv_file = "data/mood.csv"
    test_dir = "data/spectograms"

    # Create a music data module to deal with data loaders for model.
    music_dm = MusicDataModule(train_csv_file=train_csv_file,
                            train_dir=train_dir,
                            val_csv_file=validation_csv_file,
                            val_dir=validation_dir,
                            test_csv_file=test_csv_file,
                            test_dir=test_dir
                            )
    music_dm.setup(stage='train')

    for batch_idx, (image, label) in enumerate(music_dm.train_dataloader()):
        print(batch_idx, image.shape, label)
        break