# Important files in the dataset folder:

This README will describe the purpose of each function in the files inside the src/dataset folder (essentially the functions dealing with the data).

Reminder that paths involving the data folder which is not included in the repository to its fullest extent follow this structure:
```
📦data
 ┣ 📂DEAM_Annotations
 ┃ ┣ 📂annotations averaged per song
 ┃ ┃ ┣ 📂dynamic (per second annotations)
 ┃ ┃ ┃ ┣ 📜arousal.csv
 ┃ ┃ ┃ ┗ 📜valence.csv
 ┃ ┃ ┗ 📂song_level
 ┃ ┃ ┃ ┣ 📜static_annotations_averaged_songs_1_2000.csv
 ┃ ┃ ┃ ┗ 📜static_annotations_averaged_songs_2000_2058.csv
 ┃ ┗ 📂annotations per each rater 
 ┃ ┃ ┣ 📂dynamic (per second annotations)
 ┃ ┃ ┃ ┣ 📂arousal
 ┃ ┃ ┃ ┃ ┣ 📜10.csv
 ┃ ┃ ┃ ┃ ┣ 📜...
 ┃ ┃ ┃ ┃ ┗ 📜999.csv
 ┃ ┃ ┗ 📂song_level
 ┃ ┃ ┃ ┣ 📜static_annotations_songs_1_2000.csv
 ┃ ┃ ┃ ┗ 📜static_annotations_songs_2000_2058.csv
 ┣ 📂DEAM_audio
 ┃ ┗ 📂MEMD_audio
 ┃ ┃ ┣ 📜10.mp3
 ┃ ┃ ┣ 📜...
 ┃ ┃ ┗ 📜999.mp3
 ┣ 📂features
 ┃ ┣ 📜10.csv
 ┃ ┣ 📜...
 ┃ ┗ 📜999.csv
 ┣ 📂spectograms
 ┃ ┣ 📜10.png
 ┃ ┣ 📜...
 ┃ ┗ 📜999.png
 ┣ 📜mood.csv
 ┣ 📜mood_training.csv
 ┗ 📜mood_validation.csv
```

## `data_utils.py`

- `create_csv(data_path: str , new_file_path: str) -> None`: This function creates a new csv file (new_file_path) with headers [song_id, mood, valence, arousal] based on a given csv file provided by data_path. It used valence and arousal values to automatically come up with a mood type for each song. The function does not return anything.
    - An example using the DEAM dataset:
        ```
        csv_path = "data/DEAM_Annotations/annotations averaged per song/song_level/static_annotations_averaged_songs_1_2000.csv"
        
        new_csv_path = "data/mood.csv"
        create_csv(csv_path, new_csv_path)
        ```
    - This function was used to create `mood.csv`.
    - This function does not exclude the exlcuded songs.

- `create_csv_with_inputs(data_path: str, new_file_path: str) -> None`: This function does the exact same this as `create_csv()` but it lets the user set the mood of each song regardless of valence and arousal values.
    - When asked for input, if the user types *h* for a given song, that song will be labeled as happy.
    - *e* will label it as energetic.
    - *s* will label it as sad.
    - *c* will label it as calm.
    - An example using the DEAM dataset:
        ```
        csv_path = "data/DEAM_Annotations/annotations averaged per song/song_level/static_annotations_averaged_songs_1_2000.csv"
        
        new_csv_path = "data/mood.csv"
        create_csv_with_inputs(csv_path, new_csv_path)
        ```
    - This function does not exclude the exlcuded songs.

- `display_csv(csv_file_path: str) -> None`: This function will print the csv that is given to it (csv_file_path) in the format of a pandas dataframe.
    - This function will exclude the exlcuded songs.

- `csv_stats(csv_file_path: str) -> None`: This function some statistics about the given csv file (csv_file_path) as long as it contains the required headers [song_id, mood, valence, arousal].
    - An example using the DEAM dataset:
        ```
        csv_path = "data/mood.csv"
        csv_stats(csv_path)

        ### RESULTS ###
        
        Data Stats:
        There are 634 happy songs.
        There are 652 sad songs.
        There are 216 tense songs.
        There are 222 calm songs.
        There are a total of 1724 songs.

        Number of songs excluded: 20
        ```
- `train_val_split(csv_file_path: str) -> None`: This function will split the data found in csv_file_path into training and validation sets (and create csv files for both). The csv files are created in the same directory as csv file given in the arguments.
    - 200 songs from each mood type are included in the training set.
    - 16 songs from each mood type are included in the validation set.
    - Note: everytime this function is called, a different training and validation set will be created as the function randomly chooses songs.
    - This function was used to create `mood_training.csv` and `mood_validation.csv`.

## `spectograms.py`

- `generate_spectogram(audio_file_path: str) -> (np.ndarray, int)`: Returns a spectogram based on an audio file (audio_file_path) in the format of numpy array in addition to other information used for saving the spectogram as an image (the int part). Will return -1 if the audio_file_path does not exist.

- `generate_multiple_spectogram(audio_dir: str, output_dir: str) -> None`: Creates spectograms for all the audio files in audio_dir and stores them in output_dir (it will create output_dir if it doesn't exist).
    - In an effort to keep the color of the spectogram, this function will first plot the spectogram using the libraries matplotlib and librosa. It will then save the plot as a png.
        - **TODO**: Find a way to save the image without the need to plot, as plotting and using the plt.savefig() function takes a long time.
    - When the function starts and if the output_dir exists, it will not re-generate spectograms for songs that already have one.
    - This function was used to create every spectogram in the `data/spectograms/` folder.
    - This function does not exclude the exlcuded songs. It will generate spectograms for the exluded songs, however the reasons the songs are exluded is because their spectograms generated weird.
        - An example using the DEAM dataset:
        ```
        audio_dir = "data/DEAM_audio/MEMD_audio"
        output_dir = "data/spectograms"
        generate_multiple_spectogram(audio_dir, output_dir)
        ```

## `music_dataset.py`

- `class MusicDataset(torch.utils.data.Dataset)`: A custom PyTorch dataset class for managing the retrival of spectogram images and their assocaited label(s).
    
    - `__init__(self, csv_file_path: str, data_dir: str) -> None`: Takes in a path to a csv file (csv_file_path) as well as the directory where the data is stored(data_dir). The directory in this case would be the spectograms folder as that is what is being fed to the model. Turns the contents of the csv file into a pandas dataframe.
        - This function will exclude the exlcuded songs.
    
    - `print_df(self) -> None`: Prints the dataframe associated with this instance of a MusicDataset object.
    
    - `__len__(self) -> int`: Returns the number of rows (images and their labels) in the pandas dataframe.
    
    - `__getitem__(self, idx) -> (torch.Tensor, str)`: Returns the image (loaded using the cv2 library as a numpy array, then converted to a tensor) in addition to its associated mood type as a string.
    
    - An example using the DEAM dataset:
        ```
        csv_path = "data/mood.csv"
        data_dir = "data/spectograms"

        dataset = MusicDataset(csv_file_path=csv_path, data_dir=data_dir)

        print(len(dataset))
        print(dataset[0])
        dataset.print_df()
        ```

## `music_datamodule.py`

- `class MusicDataModule(pl.LightningDataModule)`: A PyTorch lightning data module for setting up training, testing, and validation datasets/dataloaders.

    - `__init__(self, train_csv_file: str, train_dir: str, val_csv_file: str, val_dir: str, test_csv_file: str, test_dir: str, batch_size: int = 4, num_workers: int = 1)`: Takes in all the paths that lead to csv files related to training, validation, and testing. In addition, it allows the user to set the batch_size of the dataloaders in addition to the number of workers.

    - `setup(self, stage: str) -> None`: Creates instances of the `MusicDataset` class based on a specific stage and stores them. Valid stages include: [train, validate, test]. This function does not return anything.

    - `train_dataloader(self) -> TRAIN_DATALOADERS`: Returns a dataloader for training based on the MusicDataset instance created using the `setup("train")` function.

    - `val_dataloader(self) -> EVAL_DATALOADERS`: Returns a dataloader for validation based on the MusicDataset instance created using the `setup("validate")` function.

    - `test_dataloader(self) -> EVAL_DATALOADERS`: Returns a dataloader for testing based on the MusicDataset instance created using the `setup("test")` function.

    - An example using the DEAM dataset:
        ```
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
        ```