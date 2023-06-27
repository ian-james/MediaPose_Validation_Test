import os
from enum import Enum

import cv2
import pandas as pd
import logging

def copy_csv_to_excel(csv_file, excel_file):
    # Copy the CSV file to an Excel file
    try:
        df = pd.read_csv(csv_file, sep="\t")
        df.to_excel(excel_file, index=False, header=True)
    except Exception as e:
        logging.error("Error copying CSV to Excel: " + str(e))


def add_extension(filename, extension=".csv"):
    basename, ext = os.path.splitext(filename)
    if ext == extension:
        return filename
    else:
        return filename + extension

def flip_image(image, should_flip):
    if(should_flip):
        image = cv2.flip(image, 1)
        should_flip = False
    return image, should_flip


def get_file_path(output_file, location="../records/"):
    # This section manages the data collection.
    absolute_path = os.path.abspath(location)
    create_directory(absolute_path)
    full_path = os.path.join(absolute_path, output_file)
    return full_path


def create_directory(directory_path):
    """
    Creates a directory at the given path if it doesn't already exist.

    Parameters:
        directory_path (str): The path to the directory to create.

    Returns:
        None
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def write_snapshot_image(filename, image):
    # Write the image to a file
    status = cv2.imwrite(filename, image)
    return status

def open_recording_file(record_file, frame_size, fps, location="../records/"):
    # Define the codec and create a VideoWriter object
    # Allow Recording only if the user previously specified a file name.
    out_record_media = None
    if(record_file != ""):
        absolute_path = os.path.abspath(location)
        create_directory(absolute_path)
        full_path = os.path.join(absolute_path, record_file)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_record_media = cv2.VideoWriter(full_path, fourcc, fps, frame_size)
    return out_record_media


def open_image(image_path):
    try:
        # Read the image file
        image = cv2.imread(image_path)

        if image is None:
            raise ValueError("Error reading image file.")

        return image

    except Exception as e:
        print(f"An error occurred opening the image: {image_path}, {str(e)}")
        return None
