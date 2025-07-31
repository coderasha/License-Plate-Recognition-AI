# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import cv2
import torch
import easyocr
from werkzeug.utils import secure_filename
from utils import detect_weather

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load EasyOCR once
ocr_reader = easyocr.Reader(['en'], gpu=False)

@app.route('/process', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        image_file = request.files['image']
        filename = secure_filename(image_file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image_file.save(filepath)

        # Load image with OpenCV
        image = cv2.imread(filepath)
        if image is None:
            return jsonify({'error': 'Invalid image'}), 400

        # OCR
        ocr_results = ocr_reader.readtext(image)
        number_plate = ''
        for (bbox, text, prob) in ocr_results:
            if prob > 0.5:  # Confidence threshold
                number_plate = text
                break

        # Weather detection
        weather = detect_weather(filepath)

        return jsonify({
            'number_plate': number_plate,
            'weather': weather
        })

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
