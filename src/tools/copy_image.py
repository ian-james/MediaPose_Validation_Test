# This is the code that generates the images for the video:
# It is a simple script that takes an image and repeats it for a specified number of frames.
# The output video is saved in the same directory as the input image.
# The output video is named as the input image name with the extension changed to .mp4.
# The number of frames to repeat the image is specified as a command line argument.
# The script can be run from the command line as follows:
# python copy_image.py --image image.jpg --output video.mp4 --num_frames 30

import cv2
import argparse

parser = argparse.ArgumentParser(description='Convert image to video')
parser.add_argument('--image', required=True, help='input image file')
parser.add_argument('--output', required=True, help='output video file')
parser.add_argument('--num_frames', type=int, default=30,
                    help='number of frames to repeat the image')


args = parser.parse_args()

# Load the image
img = cv2.imread(args.image)

# Define the output video properties
fps = 30
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(args.output, fourcc, fps, (img.shape[1], img.shape[0]))

# Repeat the same image for the specified number of frames
for i in range(args.num_frames):
    out.write(img)

# Release the video stream
out.release()
