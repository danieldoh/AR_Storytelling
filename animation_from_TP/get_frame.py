import cv2
import os

# Folder path containing video files
folder_path = './static/animation/'

# Get a list of all files in the folder with the specified extension
video_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]

# Loop through each video file and extract the first frame
for video_file in video_files:
    video_path = os.path.join(folder_path, video_file)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video file was opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_file}.")
        continue

    # Read the first frame
    ret, first_frame = cap.read()

    # Release the video capture object
    cap.release()

    # Check if the frame was read successfully
    if not ret:
        print(f"Error: Could not read frame from {video_file}.")
        continue

    # Create the output image file path
    output_path = os.path.splitext(video_path)[0] + '.png'

    # Save the first frame as a PNG image
    cv2.imwrite(output_path, first_frame)

    print(f"Saved first frame from {video_file} as {output_path}")

