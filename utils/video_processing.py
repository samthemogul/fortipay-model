import cv2
import os

def extract_first_frame(video_path, output_path):
    """ Extracts the first frame of a video and saves it as an image. """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Unable to open video file {video_path}")
        return None

    success, frame = cap.read()  # Read the first frame
    cap.release()

    if success:
        # Ensure the output folder exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        cv2.imwrite(output_path, frame)  # Save the first frame
        return output_path
    else:
        print(f"Error: Failed to extract frame from {video_path}")
        return None