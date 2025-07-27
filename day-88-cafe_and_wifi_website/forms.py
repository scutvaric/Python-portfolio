from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DecimalField, SelectField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Cafe Location URL", validators=[DataRequired(), URL()])
    img_url = StringField("Cafe Image URL", validators=[DataRequired(), URL()])
    location = StringField("Cafe Location", validators=[DataRequired()])
    has_sockets = BooleanField("Check the box if the cafe has sockets?")
    has_toilet = BooleanField("Check the box if the cafe has toilets?")
    has_wifi = BooleanField("Check the box if the cafe has wifi?")
    can_take_calls = BooleanField("Check the box if the cafe can take calls?")
    seats = SelectField("How many seats does the cafe have?",
                        choices=[
                            ("0-10", "0-10"),
                            ("10-20", "10-20"),
                            ("20-30", "20-30"),
                            ("30-40", "30-40"),
                            ("40-50", "40-50"),
                            ("50+", "50+")
                        ],
                        validators=[DataRequired()])
    coffee_price = DecimalField("What's the coffee price (in £)?", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# Create a form to register new users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


# Create a form to login existing users
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


# Create a form to add comments
class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")
