from flask import Flask, request, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
import os
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

load_dotenv("variables.env")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
API_KEY = os.environ.get('DICTIONARY_API_KEY')

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ckeditor = CKEditor(app)
Bootstrap5(app)

class WordToTranslateForm(FlaskForm):
    word = StringField(label='Word to translate', validators=[DataRequired()])
    submit = SubmitField(label="Translate")

@app.route("/", methods=['POST', 'GET'])
def home():
    form = WordToTranslateForm()
    if form.validate_on_submit():
        word_to_translate = request.form["word"]

        url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word_to_translate}?key={API_KEY}"

        response = requests.get(url)
        translation = response.json()
        print(translation)
        return render_template("index.html", form=form, results=translation)
    return render_template("index.html", form=form)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=False, port=5001)
