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

def change_filename(filepath, new_filename):
    # Get the directory and extension of the original file
    directory = os.path.dirname(filepath)
    extension = os.path.splitext(filepath)[1]

    # Create the new file path with the updated filename
    new_filepath = os.path.join(directory, new_filename + extension)
    return new_filepath


def convert_to_mp4(video_path, output_path, codec='libx264'):
    try:
        clip = VideoFileClip(video_path)
        clip.write_videofile(output_path, codec=codec,fps=12)
        clip.close()
        return True
    except Exception as e:
        st.error(
            f"Failed to convert video file named {video_path} to {output_path} with codec {codec}. {e}")
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


    st.success("Saved File:{} to tempDir".format(location))
    return location


def download_dataframe(df, file_name, file_format):
    # Create a button to download the filex
    try:
        output = BytesIO()

        if file_format == 'xlsx':
            df.to_excel(output, sheet_name="Sheet1", index=False, header=True)
            mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        elif file_format == 'csv':
            df.to_csv(output, sep='\t', index=False)
            mime_type = 'text/csv'

        output.seek(0)

        if file_format == 'xlsx':
            ext = 'xlsx'
        elif file_format == 'csv':
            ext = 'csv'

        file_label = f'Download {file_format.upper()}'
        file_download = f'{file_name}.{ext}'
        b64 = base64.b64encode(output.read()).decode()

        st.markdown(
            f'<a href="data:file/{mime_type};base64,{b64}" download="{file_download}">{file_label}</a>',
            unsafe_allow_html=True
        )
    except:
        st.error(f"Unable to generate download file: {file_name}")


def set_state_option(key, value):
    if key not in st.session_state:
        st.session_state[key] = value
    else:
        st.session_state[key] = value


def get_state_option(key):
    if key not in st.session_state:
        return None
    else:
        return st.session_state[key]


def flip_video_state(key):
    set_state_option(key, not get_state_option(key))


def allow_download_button(file_path):
    with open(file_path, 'rb') as my_file:
        st.download_button(label='Download', data=my_file, file_name='filename.xlsx',
                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


def display_download_buttons(df, file_path):
    col1, col2 = st.columns([1, 1])
    with col1:
        download_dataframe(df, file_path, "csv")
    with col2:
        download_dataframe(df, file_path, 'xlsx')


def display_video_buttons():

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        play_button = st.button("Play", key="play_btn",
                                on_click=flip_video_state('play'))
    with col3:
        stop_button = st.button("Stop", key="stop_btn")

    return play_button, stop_button


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
                flag, image = cap.read()
            
                if flag:
                    # The frame is ready and already captured            
                    pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
                else:
                    # The next frame is not ready, so we try to read it again
                    cap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame-1)
                    cv2.waitKey(1000)
                    continue
                
                fps_timer.update()
                
                if pos_frame == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                    logging.info("Finished the video.")
                    break
                                
                total_frames += 1
                if (media_only):
                    frame = draw_mediapipe(pose, image, total_frames, media_noface)
                else:
                    # Do our version of the pose estimation.
                    frame = draw_mediapipe_extended(pose, image, total_frames, False)

                    df = add_dataframe(df, frame)
                    idf = add_key_columns(idf, frame)

                with mediapipe_container.container():                    
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    st.image(image_rgb)
                        

                    with st.expander("See Data Table"):
                        if(idf is not None):
                            st.dataframe(idf, hide_index=True)

                    st.text(f"FPS: {fps_timer.get_fps()}")
            if (cap):
                cap.release()
        return df

    except Exception as e:
        logging.error(f"Failed to run streamlit main {e}")


def main():
    tmpDir = "/home/james/Projects/mediapipe_demo/MediaPose_Validation_Test/videos/"
    deploy_mode = True
    if(deploy_mode):
        tmpDir = ""

    title = st.title("HULC - Physio Mediapipe Project")

    ################################################################################
    # MediaPipe Options
    mediapipe_expander = st.sidebar.expander("## User Options", expanded=True)
    mediapipe_expander.markdown("## Mediapipe Options")

    min_detection_con = mediapipe_expander.slider(
        "Minimum detection confidence", min_value=0.0, max_value=1.0, value=0.8, step=0.1)

    min_tracking_con = mediapipe_expander.slider(
        "Minimum tracking confidence", min_value=0.0, max_value=1.0, value=0.8, step=0.1)

    desired_fps = mediapipe_expander.number_input(
        "FPS", min_value=0, max_value=60, value=0, step=1)

    fps_text = st.empty()

    st.markdown("## Program Options")
    mode_src = st.selectbox(
        "Select the mode", ['None', 'Camera Capture', 'Camera', 'Video', 'Image','Watch'])

    ################################################################################
    # Debug Options
    debug_expander = st.sidebar.expander("## Developer Options", expanded=True)
    debug_expander.markdown("## Debugging Controls")

    debug_levels = ['debug', 'info', 'warning', 'error', 'critical']
    debug_expander.selectbox("Set the logging level", debug_levels)

    media_only = debug_expander.checkbox("Mediapipe Only", value=False)
    ignore_face = debug_expander.checkbox("Ignore Face", value=False)
    
    if(mode_src=='Watch'):
        title.title("Watch Video")        
        st.divider()
        uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])
        if (uploaded_file):
            filename = save_uploadedfile(uploaded_file, tmpDir)           
            st.write(f"File is: {filename}")
            output_file = change_filename(filename, "output")
            st.write(f"Output File is: {output_file}")
            if (convert_to_mp4(filename, output_file)):
                st.video(output_file)
            else:
                st.write(f"Video file is not open {output_file}")

    elif (mode_src == 'Image'):
        title.title("Image Analysis")
        st.subheader("Analyse a single image.")
        st.divider()
        uploaded_file = st.file_uploader("Upload an image file", type=["jpg", "png", "jpeg"])
        if (uploaded_file):
            if uploaded_file is not None:
                # To read file as bytes:
                if (not deploy_mode):
                    filename = save_uploadedfile(uploaded_file, os.path.join(tmpDir, "images"))
                else:
                    filename = uploaded_file.name                    

                st.write(f"File is: {filename}")
                if (filename is not None):
                    if (deploy_mode):
                        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                        image = cv2.imdecode(file_bytes, 1)
                    else:
                        image = open_image(filename)

                    if (image is not None):
                        st.write(
                            f"Min Detection Confidence: {min_detection_con} and Min Tracking Confidence: {min_tracking_con}")
                        original_image, image, df = run_photo_analysis(
                            image, media_only, ignore_face, min_detection_con, min_tracking_con)

                        st.image(image=original_image,
                                 caption="Uploaded Image", channels="BGR")
                        st.image(image=image, caption="Enhanced Image",
                                 channels="BGR")

                        idf = get_key_frames(df)
                        st.dataframe(idf)

                        if (filename is not None):
                            display_download_buttons(
                                idf, os.path.join("image", Path(filename).stem))
                    else:
                        st.error(f"Failed to open image {uploaded_file}.")

    elif (mode_src == 'Video'):
        title.title("Video Analysis")
        st.subheader("Analyse a video file.")
        st.divider()
        # Upload the video and save it
        print("ONE")
        uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])
        print("two")
        try:
            if (uploaded_file):
                filename = save_uploadedfile(uploaded_file, tmpDir)           
                print("THREE")
                st.write(f"File is: {filename}")
                output_file = change_filename(filename, "output")
                st.write(f"Output File is: {output_file}")
                if (convert_to_mp4(filename, output_file)):
                    st.write(f"Output file exists {output_file}")
                    df = run_streamlit_video_mediapipe_main(
                        output_file, min_detection_con, min_tracking_con, desired_fps, media_only, ignore_face)
                    idf = get_key_frames(df)
                    if (df is not None):
                        st.write(output_file)
                        display_download_buttons(idf, Path(output_file).stem)
                else:
                    st.write(f"Video file is not open {output_file}")
        except Exception as e:
            print("IN THE VIDEO MODE")
            print(e)

    elif (mode_src == 'Camera Capture'):

        title.title("Image Capture")
        st.subheader("Capture an image from your camera.")
        st.divider()

        img_file_buffer = st.camera_input("Camera")
        if (img_file_buffer):
            st.write(img_file_buffer)
            if (not deploy_mode):
                filename= save_uploadedfile(img_file_buffer, os.path.join(tmpDir, "images"))
            else:
                filename = img_file_buffer.name                

            if (filename is not None):
                if (deploy_mode):
                    file_bytes = np.asarray(bytearray(img_file_buffer.read()), dtype=np.uint8)
                    image = cv2.imdecode(file_bytes, 1)
                else:
                    image = open_image(filename)

                if (image is not None):
                    st.write(f"Min Detection Confidence: {min_detection_con} and Min Tracking Confidence: {min_tracking_con}")

                    original_image, image, df = run_photo_analysis(
                        image, media_only, ignore_face, min_detection_con, min_tracking_con)                   

                    st.image(image=image, caption="Enhanced Image",
                             channels="BGR")

                    idf = get_key_frames(df)
                    st.dataframe(idf)
                    if (df is not None):
                        st.write(filename)
                        display_download_buttons(idf, Path(filename).stem)

    elif (mode_src == 'Camera'):
        title.title("Real-Time Analysis")
        st.subheader("Analyse a video stream from your camera.")
        st.divider()
        # Select a Camera option
        webrtc_streamer(key="example",
                        video_frame_callback=camera_frame_callback,
                        rtc_configuration={  # Add this line
                            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                        })


def camera_frame_callback(frame):
    try:
        img_array = frame.to_ndarray(format="bgr24")
        img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        image, df = run_camera_analysis(img, False, True, 0.8, 0.8)
    except Exception as e:
        print(e)
    return av.VideoFrame.from_ndarray(image, format="rgb24")

# Paste into main camera section if needed.
# def save_camera_frame_code():
#     title.title("Real-Time Analysis")
#     st.subheader("Analyse a video stream from your camera.")
#     st.divider()
#     # Select a Camera option
#     camera_options = find_camera()
#     if len(camera_options) > 1:
#         selected_camera = st.selectbox("Select a camera", camera_options)

#         if (selected_camera != "No Camera"):
#             camera_index = int(selected_camera.split()[1])
#             df = run_streamlit_video_mediapipe_main(
#                 camera_index, min_detection_con, min_tracking_con, desired_fps, media_only, ignore_face)
#             idf = get_key_frames(df)
#             if (idf is not None):
#                 st.write(filename)
#                 display_download_buttons(idf, Path(filename).stem)
#     else:
#         st.error("Unable to identify active camera.")


if __name__ == '__main__':
    main()
