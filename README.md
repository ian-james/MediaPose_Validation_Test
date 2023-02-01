# Project Introduction
This project examines the validity of the mediapose library against other motion analysis techniques.
Our research expands on the the Mediapipe library, particularly the shoulder positions associated with the landmark placement
Specifically, we investigate shoulder flexion, abduction, and extension and a patient performance an action.

Mediapipe Github repo and Front Page are available:
https://google.github.io/mediapipe/

https://github.com/google/mediapipe

Objective:
Our research performs a comparative analysis to validate the accuracy levels occuring in MediaPipe. Our analysis will evaluate the performance between Dartfish, Mediapipe, and higher-end solutions. Our goal is to identify inexpensive telehealth options which uphold the high-levels of standards produced within clinics or more expensive setups.

# Download Stage 
 Go to Code and click download Zip file.

# Setup Stages
 * Setup Virtual Environment - (This keeps your computer settings safe and makes it easy to add new projects.) 
 * Active Virtual Environment
 * Install requirements
 * Setup MediaPipe Models
 * Run Program

# Step 0: Setup Virtual Environment 
 python3 -m venv mp_env
 
 cd mp_env
 
# Step 1: Activiate Virtual Environment
 source mp_env/bin/activate

## To re-activate a virtual environment (if you've closed the environment.)
source mp_env/bin/activate

# Step 2: Install requirements - This will include mediapipe
pip install -r requirements.txt

## Alternatively: If you need to install only MediaPipe
pip install mediapipe

# Step 3: Setup MediaPipe Models
## Option 1) Download the Pose Landmarks Model located it at the below addres and put it a folder called models
* https://github.com/google/mediapipe/releases/download/v0.8.0/pose_landmarks_2d.tflite

Alternatively on Linux, this file can be directly downloaded and placed in the project folder within the folder called models/
curl -LJO https://github.com/google/mediapipe/releases/download/v0.8.0/pose_landmarks_2d.tflite
mv pose_landmarks_2d.tflite models/

# Step 4: Run Program
From the python environment src folder run the following command:
python test_shoulder_camera.py


