# MediaPose_Validation_Test
Mediapose validation project (Starting from Demo)


#Setup Virtual Environment
#Create a virtual environment (This keeps your computer settings safe.) 
#&& starts a second command to active the virtual environment.
python3 -m venv mp_env && source mp_env/bin/activate


#To re-activate a virtual environment use
source mp_env/bin/activate

#Install MediaPipe
pip install mediapipe

# Download the Pose Landmarks Model
curl -LJO https://github.com/google/mediapipe/releases/download/v0.8.0/pose_landmarks_2d.tflite
mv pose_landmarks_2d.tflite 
mv pose_landmarks_2d.tflite models/
