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


@app.route("/", methods=['POST', 'GET'])
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=False, port=5001)
