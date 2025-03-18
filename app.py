import os
import cv2
import json
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from collections import Counter
from utils.video_processing import extract_first_frame

load_dotenv()


app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["AZURE_PREDICTION_URL"] = os.getenv("AZURE_PREDICTION_URL")
app.config["AZURE_PREDICTION_KEY"] = os.getenv("AZURE_PREDICTION_KEY")

# Azure Custom Vision API
AZURE_PREDICTION_URL = app.config["AZURE_PREDICTION_URL"]
HEADERS = {
    "Prediction-Key": app.config["AZURE_PREDICTION_KEY"],
    "Content-Type": "application/octet-stream"
}

def send_frame_for_prediction(image_path):
    """ Sends a frame to Azure Custom Vision and returns the prediction """
    with open(image_path, "rb") as image_file:
        response = requests.post(AZURE_PREDICTION_URL, headers=HEADERS, data=image_file)
    
    if response.status_code == 200:
        print(response.json())
        return response.json()
    return None

def get_product_tag(video_path, output_folder):
    """ Extracts the first frame, sends it for prediction, and returns the product tag. """
    frame_path = os.path.join(output_folder, "first_frame.jpg")
    
    # Extract the first frame
    extracted_frame = extract_first_frame(video_path, frame_path)
    if not extracted_frame:
        return "Frame Extraction Failed"

    # Send the frame to Azure Custom Vision
    prediction = send_frame_for_prediction(frame_path)

    # Extract product tag
    if prediction and "predictions" in prediction:
        return max(prediction["predictions"], key=lambda x: x["probability"])["tagName"]

    return "Unknown"


def download_video(url, filename):
    """Downloads a video from a URL and saves it locally."""
    print(url, filename)
    response = requests.get(url, stream=True)
    print(response)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    return filepath


@app.route("/predict", methods=["POST"])
def predict():
    """ Flask API route to compare products in two videos """
    data = request.get_json()
    video1_url = data.get("seller_video")
    video2_url = data.get("buyer_video")

    if not video1_url or not video2_url:
        return jsonify({"error": "Missing video URLs"}), 400

    # Download videos (assuming they are accessible URLs)

    video1_path = download_video(video1_url, "seller.mp4")
    video2_path = download_video(video2_url, "buyer.mp4")


    # Get most frequent product in both videos
    product1 = get_product_tag(video1_path, "frames/video1")
    product2 = get_product_tag(video2_path, "frames/video2")

    print(f"Product in seller video: {product1}")
    print(f"Product in buyer video: {product2}")


    return jsonify({
        "product_seller": product1,
        "product_buyer": product2
    }), 200

if __name__ == "__main__":
    app.run(port=3000, debug=True)
