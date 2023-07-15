import threading
from streamlit_webrtc import webrtc_streamer
import av
from matplotlib import pyplot as plt
import cv2
import os
import base64
from pathlib import Path
from io import BytesIO
import numpy as np
from PIL import Image

import streamlit as st
from moviepy.editor import VideoFileClip
from opencv_file_utils import open_image
from tempfile import NamedTemporaryFile

from utils import *
from file_utils import *
from camera_utils import *
from log import *

import moviepy.editor as mp
from fps_timer import FPS

# MediaPipe Includes
import mediapipe as mp

from mediapipe_main import draw_mediapipe, draw_mediapipe_extended, handle_keyboard, mediapose_main
from photo_main import run_photo_analysis, run_camera_analysis

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def convert_to_mp4(video_path, output_path, codec='libx264'):
    try:
        clip = VideoFileClip(video_path)
        clip.write_videofile(output_path, codec=codec, fps=12)
        clip.close()
        return True
    except Exception as e:
        st.error(f"Failed to convert video file named {video_path} to {output_path} with codec {codec}. {e}")
    return False


def save_uploadedfile(uploadedfile, folder='tempDir'):
    location = uploadedfile.name
    if (folder != ""):
        location = os.path.join(folder, uploadedfile.name)
    try:
        with open(location, "wb") as f:
            f.write(uploadedfile.getbuffer())
    except:
        st.error(f"Failed to save the {location}.")
        return None


    st.success(f"Saved File:{location} to tempDir")
    return location



def run_streamlit_video_mediapipe_main(filename, min_detection_con=0.5, min_tracking_con=0.5, fps=30,
                                       media_only=False, media_noface=False):

    # Streamlit UI Options.
    mediapipe_container = st.empty()
    df = None
    idf = None
    total_frames = 0
    try:
        cap, mode, fps, frame_size = setup_video_capture(
            filename=filename, fps_rate=fps, request_filename=False)
        with FPS() as fps_timer, mp_pose.Pose(min_detection_confidence=min_detection_con, min_tracking_confidence=min_tracking_con) as pose:
            while cap.isOpened():
                success, image = cap.read()
                fps_timer.update()

                if not success:
                    if (mode == VideoMode.VIDEO):
                        logging.info("Finished the video.")
                        break
                    else:
                        logging.info("Ignoring empty camera frame.")
                        continue

                total_frames += 1
                if (media_only):
                    frame = draw_mediapipe(
                        pose, image, total_frames, media_noface)
                else:
                    # Do our version of the pose estimation.
                    frame = draw_mediapipe_extended(
                        pose, image, total_frames, False)

                    df = add_dataframe(df, frame)
                    idf = add_key_columns(idf, frame)

                with mediapipe_container.container():
                    st.image(image, channels="BGR")

                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    st.image(image_rgb)

                    with st.expander("See Data Table"):
                        if (idf is not None):
                            st.dataframe(idf, hide_index=True)

                    st.text(f"FPS: {fps_timer.get_fps()}")
            if (cap):
                cap.release()
        return df

    except Exception as e:
        logging.error(f"Failed to run streamlit main {e}")


def main():  
    title = st.title("Test Video")
    ################################################################################
    # MediaPipe Options 
    min_detection_con = st.slider("Minimum detection confidence", min_value=0.0, max_value=1.0, value=0.8, step=0.1)
    min_tracking_con = st.slider("Minimum tracking confidence", min_value=0.0, max_value=1.0, value=0.8, step=0.1)
    
    title.title("Video Analysis")
    st.subheader("Analyse a video file.")
    st.divider()
    # Upload the video and save it
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov","mpeg"])
    if (uploaded_file):    
        st.markdown("## Program Options")
        mode_src = st.selectbox("Select the mode", ['None','st_video','save_upload','tmp_upload','decode','convert'])
        ################################################################################
        if (mode_src == 'st_video'):
            st.video(uploaded_file.name)
        elif(mode_src == 'save_upload'):
            filename = save_uploadedfile(uploaded_file,"")
            st.video(filename)
        elif(mode_src == 'tmp_upload'):      
            filename = NamedTemporaryFile(delete=False)
            filename.write(uploaded_file.read())
            st.video(filename)
        elif(mode_src == 'decode'):
            video_bytes = uploaded_file.read()
            video_nparray = np.frombuffer(video_bytes, np.uint8)
            video = cv2.imdecode(video_nparray, cv2.IMREAD_UNCHANGED)
            # Display video
            st.video(video)
        elif(mode_src == 'convert'):
            output_file =  "test_output.mp4"
            filename = save_uploadedfile(uploaded_file, "")            
            if(convert_to_mp4(filename, output_file)):
                st.video(output_file)
            else:
                st.error("Failed to convert video")
            
     
if __name__ == '__main__':
    main()