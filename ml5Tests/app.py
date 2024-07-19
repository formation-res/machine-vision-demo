from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__, static_url_path='/static')
CORS(app)  # This will enable CORS for all routes
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = ResNet50(weights='imagenet')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/classify', methods=['POST'])
def upload_file():
    # find uploaded file
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part in the request'}), 400

    file = request.files['file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400

    # temporarily save file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # run model
    try:
        predictions = predict(file_path)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

    # delete file
    try:
        os.remove(file_path)
        print("File deleted successfully")
    except Exception as e:
        print(f"Error deleting file: {e}")
        return jsonify({'success': False, 'error': 'Error deleting file'}), 500

    # package and return results to javascript
    result = {"message": "Python function called successfully", "data": predictions}
    print("final results: ", result)
    
    return jsonify(result)

def predict(img_path):
    # load image
    img = image.load_img(img_path, target_size=(224, 224))

    # preprocess for keras model
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # predict processed image
    preds = model.predict(x)
    predictions = decode_predictions(preds, top=3)[0]
    print('Predicted:', predictions)

    # return predicted classes in a string
    response = f"{predictions[0][1]} or {predictions[1][1]} or {predictions[2][1]}"
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5500)