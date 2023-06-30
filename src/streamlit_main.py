
from moviepy.editor import VideoFileClip
import streamlit as st
import os
import cv2
import numpy as np


from utils import *
from camera_utils import *
from log import *

from PIL import Image
import moviepy.editor as mp
from streamlit_webrtc import webrtc_streamer
import av

def change_filename(filepath, new_filename):
    # Get the directory and extension of the original file
    directory = os.path.dirname(filepath)
    extension = os.path.splitext(filepath)[1]

    # Create the new file path with the updated filename
    new_filepath = os.path.join(directory, new_filename + extension)
    return new_filepath
    
    return True
def convert_to_mp4(video_path, output_path, codec='libx264'):
    try:
        clip = VideoFileClip(video_path)
        clip.write_videofile(output_path, codec=codec)
        clip.close()
        print("Video conversion successful!")
        return True
    except Exception as e:
        print(f"Failed to convert video file named {video_path} to {output_path} with codec {codec}. {e}")
        
    return False

def main():
    st.title("Video Player with Drawing")      

    ################################################################################
    # MediaPipe Options
    st.sidebar.markdown("## MediaPipe Options")

    st.sidebar.slider("Minimum detection confidence",
                      min_value=0.0, max_value=1.0, value=0.8, step=0.1)

    st.sidebar.slider("Minimum tracking confidence",
                      min_value=0.0, max_value=1.0, value=0.8, step=0.1)
    
    ################################################################################
    # Program Options
    st.sidebar.markdown("## Program Options")
    mode_src = st.sidebar.selectbox(
        "Select the mode", ['Camera', 'Video', 'Image'])
    if (mode_src == 'Image'):
        uploaded_file = st.file_uploader("Upload an image file", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            # To read file as bytes:
            st.write(f"The file is {uploaded_file}")
            image = Image.open(uploaded_file)
            st.image(image=image, caption="Uploaded Image")

    elif (mode_src == 'Video'):
        uploaded_file_object = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

        if (uploaded_file_object):
            # os.path.join(, selected_filename)
            
            uploaded_file = os.path.join("./videos/tests/", uploaded_file_object.name)
            st.success(f"File selected: {uploaded_file}")

            output_file = change_filename(uploaded_file, "test_output")
            st.write(f"Output file: {output_file}")

            res = convert_to_mp4(uploaded_file, output_file)

            if (res):
                st.success(f"{uploaded_file} successfully converted.")
                st.write(f"File changed: {output_file}")
            else:
                st.error(f"{uploaded_file} failed to convert.")
            
            file = output_file
            if os.path.exists(file):
                st.write(f"Output file exists {file}")
                video_file = open(file, 'rb')
                if (video_file):
                    st.write("Video file is open")
                    video_bytes = video_file.read()
                    st.video(video_bytes)
                else:
                    st.write(f"Output file does not exist {file}")
            else:
                st.write(f"Video file is not open {output_file}")
                
                
    ############################################################################
    # Recording Options and non-file upload.
    record = st.sidebar.checkbox("Record the video", value=False)
    save_file = None
    if (record):
        save_file = st.sidebar.text_input("Enter the file name", value="record_video.mp4")

    comparative_mode = st.sidebar.checkbox(
        "Compare two video mode", value=False)

    mode_src2 = st.sidebar.selectbox("Select second Source:", [
                                     'Off', 'Camera' 'Video', 'Image'])
    if (mode_src2 != 'Off'):
        st.failure("Not implemented yet.")

    take_snapshot = st.sidebar.button("Take Snapshot")
    
    ################################################################################
    # Debug Options
    st.sidebar.markdown("## Debugging Controls")

    debug_levels = ['debug', 'info', 'warning', 'error', 'critical']
    st.sidebar.selectbox("Set the logging level", debug_levels)

    if (st.sidebar.checkbox("Mediapipe Only", value=False)):
        st.sidebar.checkbox("Ignore Face", value=False)

    st.sidebar.checkbox("Check FPS option", value=False)

    
if __name__ == '__main__':
    main()
