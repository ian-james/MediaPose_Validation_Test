# This utility file is used to store functions that are used in multiple files.
# It includes functions specific to mediapipe managing data.

from collections import OrderedDict
from datetime import datetime, timezone
import pandas as pd

def setup_frame_data(fps_count):
    # This section manages the data collection.
    odict = OrderedDict()
    odict['fps_count'] = fps_count
    odict['timestamp'] = datetime.now(
        timezone.utc).isoformat()
    return odict

def save_to_csv(df, output_file):
    """
    Appends or saves new data to an Excel file using pandas DataFrame.

    :param df: pandas DataFrame to append to, or an empty DataFrame to create
    :param output_file: name of the output Excel file
    :param interval: interval at which to save data (0 to save after each append)
    """
    sep = "\t"
    df.to_csv(output_file, index=False, header=True, sep=sep)


def add_dataframe(df, frame_data):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame([frame_data], columns=frame_data.keys())
    else:
        sfd = pd.DataFrame([frame_data], columns=frame_data.keys())
        df = pd.concat( [df,sfd], ignore_index=True,)
    return df


def get_key_frames(df):
    if df is not None and not df.empty:
        cols = df.columns
        key_columns = ['fps_count', 'timestamp', 'flexion_left',
                    'flexion_right', 'abduction_left', 'abduction_right']
        # Select only the key_columns from the data frame if they exist.
        df = df.loc[:, df.columns.isin(key_columns)]
    return df

def add_key_columns(idf, frame):
    idf = add_dataframe(idf, frame)
    return get_key_frames(idf)