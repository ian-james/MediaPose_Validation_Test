# This utility file is used to store functions that are used in multiple files.
# It includes functions specific to mediapipe managing data.

import os
import time
from enum import Enum
from collections import OrderedDict
from datetime import datetime, timezone

import cv2
import pandas as pd
import logging

from shoulder_calculations import extract_pose_frames

def setup_frame_data(fps_count):
    # This section manages the data collection.
    odict = OrderedDict()
    odict['fps_count'] = fps_count
    odict['timestamp'] = datetime.now(
        timezone.utc).isoformat()
    return odict


# This section manages the data collection.
def stores_frame_data(shoulder_info, fps_count):
    # This section manages the data collection.
    odict = setup_frame_data(fps_count)
    frame = extract_pose_frames(shoulder_info)
    odict.update(frame)
    return odict


def save_to_csv(df, frame_data, output_file):
    """
    Appends or saves new data to an Excel file using pandas DataFrame.

    :param df: pandas DataFrame to append to, or an empty DataFrame to create
    :param frame_data: list of dictionaries representing rows to append
    :param output_file: name of the output Excel file
    :param interval: interval at which to save data (0 to save after each append)
    """
    # TODO: Fix this so that it's appending and not overwriting.

    sep = "\t"
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame()
    if df.empty:
        df = pd.DataFrame(frame_data)
        df.to_csv(output_file, index=False, header=True, sep=sep)
    else:
        df = df.append(frame_data, ignore_index=True)
        #if interval == 0 or len(df) % interval == 0:
        df.to_csv(output_file, index=False, header=True, sep=sep)
    return df


def save_key_columns(df, output_file):
    key_columns = ['fps_count', 'timestamp',
                   'shoulder_left', 'shoulder_right', 'shoulder_center',
                   'elbow_left', 'elbow_right', 'elbow_center',
                   'hip_left', 'hip_right', 'hip_center',
                   'wrist_left', 'wrist_right', 'wrist_center',
                   'shoulder_flexion', 'shoulder_abduction']

    # Select only the key_columns from the data frame if they exist.
    ndf = df.loc[:, df.columns.isin(key_columns)]
    df.to_csv(output_file, index=False, header=True, sep="\t")
