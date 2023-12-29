# Music Analyzer
Creates an AI model using ResNet that will be able to detect various moods of songs. These moods include: happy, sad, calm, and tense/energetic. Essentially, audio is visualized as a spectogram (in color to be specific) and given to the AI model. The model will then learn what a spectogram looks like and associate it with a specific mood type (basically supervised learning).


## Important definitions:

- **Valence**: being positive or negative. High valence is positive, low valence is negative.
- **Arousal**: emotionally stimulating or active.

[Source - Royal Society Publishing](https://royalsocietypublishing.org/doi/10.1098/rsbl.2012.0374)

## Valence and Arousal Mood Type Table:

<div align="center">

|                  | **Low Arousal** | **High Arousal** |
|:----------------:|:---------------:|:----------------:|
|  **Low Valence** |       Sad       |       Calm       |
| **High Valence** |      Happy      |  Tense/Energetic |
|                  |                 |                  |

</div>


## Purposes of Each Important File:

- `data_utils.py`: The functions in this file are desgined to work with/create csv files based off the DEAM dataset. For example, it can automatically or manually add mood type (happy, sad, calm, tense/energetic) to a song based on certain valence and arousal values. In addition, it can display stats about the data as well as split the data into both training and validation sets.
- `spectograms.py`: An important set of functions that are used to generate spectograms of the DEAM audio. You can either generate a spectogram one at a time or generate multiple at once. The spectograms of each song are not provided and they do take a while to generate. Generating spectograms are saved as a png in color. They are the data being fed into the ResNet model.
- `music_dataset.py`: Creates a custom PyTorch dataset class for the DEAM music dataset. It takes in a csv file containing the file name in addition to other associated metadata and allows for the data to be indexed.
- `music_datamodule.py`: Creates a PyTorch Lightning data module class for setting up dataloaders for training, validation, and testing sets.
- `resnet.py`: TODO

## Data:

The audio files, in addition to their valence and arousal values (the metadata), can be downloaded [here on Kaggle](https://www.kaggle.com/datasets/imsparsh/deam-mediaeval-dataset-emotional-analysis-in-music/data). The official website for the DEAM dataset can be found [here](https://cvml.unige.ch/databases/DEAM/), however it looks like the links don't work anymore.

For this project, the static annotations averaged per song was used. Specifically, the files `static_annotations_averaged_songs_1_2000.csv` and `static_annotations_averaged_songs_2000_2058.csv` contained all the metadata used to train the AI model.

The csv files created during this project have been included in this repository. These files were made using the functions in `data_utils.py`.
- `mood.csv`: Contains the song name and mood type of associated with that song based on valence and arousal.
- `mood_training.csv`: A subset of the songs in `mood.csv` used to train the model. There are 800 songs in this subset (200 for each mood type).
- `mood_validation.csv`: A susbet of the songs in `mood.csv` (different then the ones in the training set) that is used for validation. There are 65 songs in this subset.

*Side note: This project uses all songs except 137, 146, 187, 206, 236, 449, 488, 621, 646, 661, 707, 1016, 1109, 1134, 1142, 1161, 1167, 1171, 1184, 1429 as there were issues generating their spectograms.*



## Notes:

- All file paths written don't include the root. The root is added in each function as it is needed. For writing file paths, the only necessary parts is everything after the folder Music-Analyzer.


## References:

- Code from [this](https://github.com/UC-Irvine-CS175/final-project-gan-guardians.git) GitHub repository I worked on was modified to fit this project.
