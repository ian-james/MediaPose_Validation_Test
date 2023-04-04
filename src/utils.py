import cv2
import time
from enum import Enum

# ******************************************* Global Sections
debug_mode = False
# ******************************************* End Global Sections
class VideoMode(Enum):
    CAMERA = 0
    VIDEO = 1

def setup_video_capture(filename="", fps_rate=30):
    # Check if the user chose a video file
    # Ask the user to input the video file name
    mode = VideoMode.VIDEO
    if( not filename ):
        filename = input("Enter the video file name (or enter to use camera): ").strip()

    if(not filename):
        # Open the video mode
        # Find Camera to find the right camera.
        # This is a hack to find the right camera when multiple cameras are connected.
        filename = 2
        #find_camera()
        mode = VideoMode.CAMERA

    cap = cv2.VideoCapture(filename)
    if(not cap.isOpened()):
        raise ("FAILED TO LOAD VIDEO filename= '", filename,"'")
    else:
        max_fps = cap.get(cv2.CAP_PROP_FPS)
        debug_print("MAXIMUM FPS=", max_fps)
        if(fps_rate == 0):
            fps_rate = max_fps
        else:
            cap.set(cv2.CAP_PROP_FPS, fps_rate)


    return cap, mode, fps_rate

# print arguments only when debug is enabled.
def debug_print(*args):
    global debug_mode
    if(debug_mode):
        print(*args)

# calculate the frames per second of the running video stream.
def calculate_fps():
    global fps, fps_count, start_time
    fps_count += 1
    if (time.time() - start_time) > 1:
        fps = fps_count
        fps_count = 0
        start_time = time.time()
    return fps

# Display the FPS on the screen.
def display_fps(image, fps):
    cv2.putText(image, "FPS: {:.2f}".format(
        fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# Find the camera index.
def find_camera():
    cams_test = 500
    for i in range(0, cams_test):
        cap = cv2.VideoCapture(i)
        test, frame = cap.read()
        if test:
            debug_print("i : "+str(i)+" /// result: "+str(test))
