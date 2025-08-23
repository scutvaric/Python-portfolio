from datetime import datetime
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreateTaskForm, RegisterForm, LoginForm
import os
from dotenv import load_dotenv
load_dotenv("variables.env")


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///tasks.db")
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES
class Task(db.Model):
    __tablename__ = "task"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author = relationship("User", foreign_keys=[author_id], back_populates="tasks")

    task: Mapped[str] = mapped_column(String(250), nullable=False)

    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    task_completed: Mapped[bool] = mapped_column(Boolean, default=False)

    completed_by_author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    completed_by_author = relationship("User", foreign_keys=[completed_by_author_id], back_populates="completed_tasks")


# Create a User table for all your registered users
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))

    tasks = relationship("Task", foreign_keys="Task.author_id", back_populates="author")
    completed_tasks = relationship("Task", foreign_keys="Task.completed_by_author_id",
                                   back_populates="completed_by_author")


with app.app_context():
    db.create_all()



def login_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if not current_user.is_authenticated:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function

# Register new users into the User database
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        # Check if user email is already present in the database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for("get_all_tasks"))
    return render_template("register.html", form=form, current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_tasks'))

    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_tasks'))


@app.route('/', methods=["GET"])
def get_all_tasks():
    query = Task.query

    # Apply filters
    author = request.args.get('author')
    sort = request.args.get('sort')

    if author:
        query = query.join(Task.author).filter(User.name == author)

    status = request.args.get('status', 'incomplete')  # default to incomplete
    if status == 'completed':
        query = query.filter(Task.task_completed.is_(True))
    elif status == 'incomplete':
        query = query.filter(Task.task_completed.is_(False))

    if sort == 'date_asc':
        query = query.order_by(Task.date.asc())
    elif sort == 'date_desc':
        query = query.order_by(Task.date.desc())
    elif sort == 'due_asc':
        query = query.order_by(Task.due_date.asc())
    elif sort == 'due_desc':
        query = query.order_by(Task.due_date.desc())
    elif sort == 'author':
        query = query.join(Task.author).order_by(User.name.asc())

    tasks = query.all()
    all_users = db.session.query(User).order_by(User.name).all()

    return render_template("index.html",
                           all_tasks=tasks,
                           all_users=all_users,
                           current_user=current_user,
                           query_params=request.args)

@app.route("/update_task/<int:task_id>", methods=["POST"])
@login_only
def update_task(task_id):
    task = Task.query.get_or_404(task_id)

    # Only allow the task owner or admin (user id 1)
    if task.author != current_user and current_user.id != 1:
        abort(403)

    action = request.form.get("action")

    if action == "save":
        # Update due date
        new_due_date = request.form.get('due_date')
        if new_due_date:
            task.due_date = datetime.strptime(new_due_date, '%Y-%m-%d')

        # Update task title
        new_title = request.form.get('task_title')
        if new_title:
            task.task = new_title

    elif action == "confirm":
        task.task_completed = True
        task.completed = True

    db.session.commit()
    return redirect(url_for("get_all_tasks"))


@app.route("/new-task", methods=["GET", "POST"])
@login_only
def add_new_task():
    form = CreateTaskForm()
    if form.validate_on_submit():
        new_task = Task(
            task=form.task.data,
            author=current_user,
            date=datetime.today(),
            due_date=form.due_date.data
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("get_all_tasks"))
    return render_template("add-task.html", form=form, current_user=current_user)


# Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:task_id>", methods=["GET", "POST"])
@login_only
def edit_task(task_id):
    task = db.get_or_404(Task, task_id)
    edit_form = CreateTaskForm(
        task= task.task,
        date=task.date,
        due_date=task.due_date,
        author=task.author,

    )
    if edit_form.validate_on_submit():
        task.task = edit_form.task.data
        task.due_date = edit_form.due_date.data
        task.author = current_user
        db.session.commit()
        return redirect(url_for("get_all_tasks", task_id=task.id))
    return render_template("add-task.html", form=edit_form, is_edit=True, current_user=current_user)


# Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:task_id>")
@admin_only
def delete_task(task_id):
    task_to_delete = db.get_or_404(Task, task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_tasks'))


@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


if __name__ == "__main__":
    app.run(debug=False, port=5001)