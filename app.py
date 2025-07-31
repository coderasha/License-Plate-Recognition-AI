from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from PIL import Image
import easyocr
import torch
import os

app = Flask(__name__)
CORS(app)

reader = easyocr.Reader(['en'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    image.save('temp.jpg')

    try:
        # OCR
        result = reader.readtext('temp.jpg')
        license_plate = ""
        for detection in result:
            text = detection[1]
            if len(text) >= 6 and any(char.isdigit() for char in text):
                license_plate = text
                break

        if not license_plate:
            license_plate = "Could not detect"

        # Dummy weather detection
        weather = "cloudy"  # Placeholder for now

        return jsonify({
            'plate': license_plate,
            'weather': weather
        })

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
