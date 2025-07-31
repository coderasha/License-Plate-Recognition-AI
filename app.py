from flask import Flask, render_template, request
from flask_cors import CORS
from utils import process_image
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        file = request.files.get('image')
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            result = process_image(filepath)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    print("🚀 Flask app running at http://127.0.0.1:5000")
    app.run(debug=True)
