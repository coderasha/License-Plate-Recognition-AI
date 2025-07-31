from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import easyocr
from utils import detect_weather

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

reader = easyocr.Reader(['en'])  # Initialize OCR reader

@app.route("/process", methods=["POST"])
def process_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Run OCR to read license plate
    ocr_results = reader.readtext(filepath, detail=0)
    plate_text = max(ocr_results, key=len) if ocr_results else "Not Detected"

    # Predict weather condition
    weather = detect_weather(filepath)

    return jsonify({
        "plate": plate_text,
        "weather": weather
    })

if __name__ == "__main__":
    app.run(debug=True)
