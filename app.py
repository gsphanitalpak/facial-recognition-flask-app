from flask import Flask, request, jsonify, render_template
import cv2 as cv
import numpy as np
import insightface
import tempfile
import os
import joblib
import base64
from io import BytesIO
import matplotlib

# Disable GUI backend of Matplotlib (important!)
matplotlib.use('Agg')

app = Flask(__name__)

# Initialize InsightFace model once when the app starts
insight_model = insightface.app.FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
insight_model.prepare(ctx_id=0)

# Load the trained classifier using joblib
try:
    classifier_model = joblib.load('models/svm_insightface.pkl')  # Using joblib to load the model
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")

# Function to save image as base64
def encode_image_to_base64(image):
    _, buffer = cv.imencode('.png', image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    return image_base64

# Function to draw rounded rectangles and show predictions
def draw_more_rounded_rectangle(img, pt1, pt2, color, thickness=2):
    x1, y1 = pt1
    x2, y2 = pt2
    width = x2 - x1
    height = y2 - y1
    radius = int(min(width, height) * 0.4)  # 40% of smaller side

    # Draw straight lines
    cv.line(img, (x1 + radius, y1), (x2 - radius, y1), color, thickness)
    cv.line(img, (x1 + radius, y2), (x2 - radius, y2), color, thickness)
    cv.line(img, (x1, y1 + radius), (x1, y2 - radius), color, thickness)
    cv.line(img, (x2, y1 + radius), (x2, y2 - radius), color, thickness)

    # Draw four arcs
    cv.ellipse(img, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, thickness)
    cv.ellipse(img, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, thickness)
    cv.ellipse(img, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, thickness)
    cv.ellipse(img, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, thickness)

# Prediction and visualization logic
def predict_and_visualize(image_path, model, threshold=0.5):
    image = cv.imread(image_path)
    if image is None:
        print(f"Error loading image: {image_path}")
        return None

    rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    image_height, image_width = image.shape[:2]

    faces = insight_model.get(rgb_image)
    if len(faces) == 0:
        print("No faces detected.")
        return None

    for face in faces:
        embedding = face.normed_embedding
        bbox = face.bbox.astype(int)
        left, top, right, bottom = bbox[0], bbox[1], bbox[2], bbox[3]

        probs = model.predict_proba([embedding])[0]
        best_idx = np.argmax(probs)
        confidence = probs[best_idx]
        name = model.classes_[best_idx] if confidence > threshold else "Unknown"

        draw_more_rounded_rectangle(image, (left, top), (right, bottom), color=(0, 255, 0), thickness=2)

        font_scale = image_width / 800.0
        thickness_text = 2
        font = cv.FONT_HERSHEY_SIMPLEX
        label_text = f"{name} ({confidence:.2f})"
        (text_width, text_height), _ = cv.getTextSize(label_text, font, font_scale, thickness_text)

        text_x = left
        text_y = bottom + text_height + 10
        if text_y > image_height - 10:
            text_y = bottom - 10

        cv.putText(image, label_text, (text_x, text_y), font, font_scale, (0, 255, 0), thickness_text, cv.LINE_AA)

    # IMPORTANT: Don't try to plt.show() or display GUI popup!
    return encode_image_to_base64(image)

# ROUTES
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_api():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded.'}), 400

    image = request.files['image']

    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp:
        temp_path = temp.name
        image.save(temp_path)

    result_image_base64 = predict_and_visualize(temp_path, classifier_model)

    os.remove(temp_path)

    if result_image_base64 is None:
        return jsonify({'error': 'Prediction failed, no faces detected or image issue.'}), 400

    return jsonify({'image': result_image_base64})

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
