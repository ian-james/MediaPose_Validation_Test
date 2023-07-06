import os
from enum import Enum
import time

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


def setup_fullpath_to_timestamp_output(output_filename, add_timestamp, directory="../records/"):
   # Write the DataFrame to an Excel file
    file_time = time.strftime("%Y_%m_%d-%H_%M_%S_")

    if(add_timestamp):
        ofile = file_time + output_filename
    else:
        ofile = output_filename

    path_to_file = get_file_path(ofile, directory)
    output_full_file = add_extension(path_to_file)

    return output_full_file, path_to_file