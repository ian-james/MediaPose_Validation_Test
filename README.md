# Project Introduction
This project examines the validity of the mediapose library against other motion analysis techniques.
Our research expands on the the Mediapipe library, particularly the shoulder positions associated with the landmark placement
Specifically, we investigate shoulder flexion, abduction, and extension and a patient performance an action.

Mediapipe Github repo and Front Page are available:
https://google.github.io/mediapipe/

https://github.com/google/mediapipe

Objective:
Our research performs a comparative analysis to validate the accuracy levels occuring in MediaPipe. Our analysis will evaluate the performance between Dartfish, Mediapipe, and higher-end solutions. Our goal is to identify inexpensive telehealth options which uphold the high-levels of standards produced within clinics or more expensive setups.

# Pre-Req and Download Stage 
  If you don't have Python version 3.9 or higher install on your machine, please download.
  
  ## GitHub Download
  You can download the entire project for this code by going to the Code button on right of this section.
  There you can download or clone (for developers) the project for review.
  

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

# Step 2: Install requirements - This includes all requirements for this project (including mediapipe)
pip install -r requirements.txt

## Alternatively: If you need to install only MediaPipe
pip install mediapipe

# Step 3: Setup MediaPipe Models (Optional if model does not exist in models folder)
There are three options lite,medium, and heavy. They indicate the accuracy level. 
Our current model is from 0.8.0 and should be called pose-landmarks_2d.tflite.


## Option 1) Download the Pose Landmarks Model located it at the below addres and put it a folder called models

* https://google.github.io/mediapipe/solutions/models 

Alternatively on Linux, this file can be directly downloaded and placed in the project folder within the folder called models/
curl -LJO https://github.com/google/mediapipe/releases/download/v0.8.0/pose_landmarks_2d.tflite
mv pose_landmarks_2d.tflite models/

# Step 4: Run Program
From the python environment go to the /src folder and run the following command:
python main.py

## Run Help
python main.py -h
