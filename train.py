# from ultralytics import YOLO
# import cv2
# import torch

# # Load a pre-trained YOLOv8 model
# model = YOLO("runs/detect/train2/weights/best.pt")  # You can use yolov8s.pt, yolov8m.pt for bigger models

# # Train the model
# # model.train(
# #     data="./datasets/data.yaml",  
# #     epochs=50,  
# #     imgsz=640,  
# #     batch=8,  
# #     workers=4,  
# #     device="cpu"  # Use "cpu" if no GPU available
# # )

# # metrics = model.val()
# # print(metrics)
# results = model("shoe2.jpeg")
# for result in results:
#     im_array = result.plot()
#     im = cv2.cvtColor(im_array, cv2.COLOR_RGB2BGR)
#     cv2.imwrite("output.jpg", im)


# # from ultralytics import YOLO
# # import cv2

# # # Load your trained YOLO model
# # model = YOLO("runs/detect/train8/weights/best.pt")

# # # Define input and output video paths
# # input_video_path = "shoe.mp4"  # Change to your input video path
# # output_video_path = "output.mp4"

# # # # Open the input video
# # cap = cv2.VideoCapture(input_video_path)

# # # # Get video properties
# # frame_width = int(cap.get(3))
# # frame_height = int(cap.get(4))
# # fps = int(cap.get(cv2.CAP_PROP_FPS))
# # if fps == 0:
# #     fps = 30

# # # # Define codec and create VideoWriter object
# # fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or 'XVID' for .avi files
# # out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# # while cap.isOpened():
# #     ret, frame = cap.read()
# #     if not ret:
# #         break  # Stop if end of video

# #     # Run YOLO on the frame
# #     results = model(frame)

# #     # Draw detections on the frame
# #     annotated_frame = cv2.cvtColor(results[0].plot(), cv2.COLOR_RGB2BGR)


# #     # Write frame to output video
# #     out.write(annotated_frame)

    

# # # Release resources
# # cap.release()
# # out.release()
# # cv2.destroyAllWindows()

# # print(f"Processed video saved at: {output_video_path}")


import os
import requests

from app import UPLOAD_FOLDER


def download_video(url, filename):
    """Downloads a video from a URL and saves it locally."""
    response = requests.get(url, stream=True)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    return filepath


download_video("https://res.cloudinary.com/di1uklizr/video/upload/v1742009189/shoe_mjmgo3.mp4", "sample.mp4")

