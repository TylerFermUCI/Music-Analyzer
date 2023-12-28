"""
Functions for generating spectograms.
"""

import os
import sys
import cv2
import librosa
import pyprojroot
import numpy as np
import matplotlib.pyplot as plt

# Make it to where paths only need to be from the repo folder.
root = pyprojroot.find_root(pyprojroot.has_dir(".git"))
sys.path.append(str(root))


def generate_spectogram(audio_file_path: str) -> (np.ndarray, int):
    """
    Create a spectogram based on the audio in the audio_file_path.

    Arguments:
        audio_file_path (str): Path to a specific audio file (ex: mp3).
    
    Return value: (np.ndarray, int) if audio file exists, -1 otherwise.
    """
    # Merge root and audio_file_path.
    new_file_path = os.path.join(root, audio_file_path)

    # If audio file exists, generate a spectogram for it.
    if os.path.exists(new_file_path):
        # Load audio and create spectogram.
        x, sr = librosa.load(new_file_path, sr=44100)
        Xdb = librosa.amplitude_to_db(abs(librosa.stft(x)))
        return (Xdb, sr)
    # Could not find file.
    else:
        print(f"Audio file [{audio_file_path}] not found.")
        return -1


def generate_multiple_spectogram(audio_dir: str, output_dir: str) -> None:
    """
    Generate spectograms for all audio files in a directory.

    Arguments:
        audio_dir (str): Directory that contains all audio files.
        output_dir (str): Directory to store the images of spectograms.
    
    Return value: None
    """
    # Get a list of all audio files in the given directory.
    audio_path = os.path.join(root, audio_dir)
    list_of_audio = os.listdir(audio_path)
    
    # Create a place to store spectogram images.
    ignore = []
    out_dir_spectogram = os.path.join(root, output_dir)
    if not os.path.exists(out_dir_spectogram): os.makedirs(out_dir_spectogram, exist_ok=True)
    else: ignore = [os.path.splitext(file)[0] for file in os.listdir(output_dir)]
    # Go through the directory of audio files and create spectograms for each file.
    print(ignore)
    print("Number of current files:", len(ignore))
    print("Files to go:", len(list_of_audio) - len(ignore))
    skipped = []
    for file in list_of_audio:
        # If the file already exists, then ignore it and move on.
        if os.path.splitext(file)[0] in ignore: continue
        # Otherwise, make spectogram.
        print(f"Generating spectogram for file: {file}")
        current = os.path.join(audio_path, file)
        result, sr = generate_spectogram(current)
        # Save the image to the output directory.
        if type(result) == np.ndarray:
            new_image_name = os.path.join(out_dir_spectogram, f"{os.path.splitext(file)[0]}.png")
            #plt.figure(figsize=(14, 5))
            plt.axis('off')
            librosa.display.specshow(result, sr=sr)
            plt.savefig(new_image_name, bbox_inches='tight', pad_inches=0.0)
            #cv2.imwrite(new_image_name, cv2.cvtColor(result, cv2.COLOR_GRAY2RGB))
        # Keep track of files where a spectogram could not be generated.    
        else: skipped.append(file)
    
    # Print messages about any skipped files.
    if skipped == []: print(f"Every file in audio directory [{audio_dir}] generated a spectogram.")
    else: print(f"Files {skipped} where skipped in audio directory [{audio_dir}]")


if __name__ == "__main__":
    audio_dir = "data/DEAM_audio/MEMD_audio"
    output_dir = "data/spectograms"
    generate_multiple_spectogram(audio_dir, output_dir)
