from flask import Flask, request, render_template, url_for
from imageio.v2 import imread
import numpy as np
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from sklearn.cluster import KMeans

load_dotenv("variables.env")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ckeditor = CKEditor(app)
Bootstrap5(app)


def get_dominant_colors(image_array, n_colors=10):
    # Reshape the image to (num_pixels, 3)
    pixels = image_array.reshape(-1, image_array.shape[-1])

    # Remove alpha if present
    if pixels.shape[1] == 4:
        pixels = pixels[pixels[:, 3] == 255][:, :3]

    kmeans = KMeans(n_clusters=n_colors, n_init=10, random_state=42)
    kmeans.fit(pixels)

    rgb_colors = kmeans.cluster_centers_.astype(int)
    hex_colors = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in rgb_colors]

    return hex_colors

@app.route("/", methods=['POST', 'GET'])
def home():
    image_url = None
    top_colors = None
    uploaded_file = request.files.get('image')

    if uploaded_file and uploaded_file.filename != '':
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(file_path)

        image_array = imread(file_path)
        print(image_array)
        top_colors = get_dominant_colors(image_array, n_colors=10)
        image_url = url_for('static', filename=f'uploads/{filename}')

    return render_template("index.html", image_url=image_url, top_colors=top_colors)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=False, port=5001)
