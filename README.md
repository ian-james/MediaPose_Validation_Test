# MediaPose_Validation_Test
Mediapose validation project (Starting from Demo)

# Setup Virtual Environment
 (This keeps your computer settings safe and makes it easy to add new projects.) 
 python3 -m venv mp_env
 cd mp_env
 source mp_env/bin/activate

#To re-activate a virtual environment (if you've closed the environment.)
source mp_env/bin/activate

#Install MediaPipe
pip install mediapipe

# Download the Pose Landmarks Model and Put it a folder called models
curl -LJO https://github.com/google/mediapipe/releases/download/v0.8.0/pose_landmarks_2d.tflite
## Move the tflite (Model file) to the folder models.
mv pose_landmarks_2d.tflite models/
