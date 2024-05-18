from blog_app import app, article_dict
from flask import render_template, url_for, redirect, request, session
from werkzeug.security import generate_password_hash
import json
from wtforms import StringField, PasswordField, TextAreaField, validators
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from datetime import datetime
import uuid
from flask_wtf.csrf import CSRFProtect
from functools import wraps
from config import Config
from config import ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename
import os

app.config.from_object(Config)
csrf = CSRFProtect(app)

class Registration(FlaskForm):
    username = StringField("username", [validators.Length(min=4, max=15), validators.DataRequired()])
    password = PasswordField("password", [
        validators.Length(min=6, max=14), validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField("repeat password")

class Login(FlaskForm):
    username = StringField("username", [validators.Length(min=4, max=15), validators.DataRequired()])
    password = PasswordField("password", [validators.Length(min=6, max=14), validators.DataRequired()])

class Article(FlaskForm):
    title = StringField('title', [validators.Length(min=10), validators.DataRequired()])
    description = StringField('description', [validators.Length(min=30), validators.DataRequired()])
    date = datetime.now().strftime('%d %b %y')
    article_text = TextAreaField('Text', render_kw={"rows": 20, "cols": 100}, validators=[validators.DataRequired()])
    file = FileField("image", validators=[validators.DataRequired()])

def validate(form):
    if form['username'] == article_dict['admin']['username'] and form['password'] == article_dict['admin']['password']:
        return True
    else:
        return False

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def get_latest_item_key(dictionary):
    latest_date = None
    latest_key = None

    for key, value in dictionary.items():
        date_string = value.get('date_written', '')  # Get the date string from the dictionary
        if date_string:
            # Convert the date string to a datetime object
            date = datetime.strptime(date_string, '%d %b %y')

            # Check if the current item is newer than the latest item
            if latest_date is None or date > latest_date:
                latest_date = date
                latest_key = key

    return latest_key




def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    latest = get_latest_item_key(article_dict)
    return render_template("public/index.html", articles=article_dict, latest=latest)

@app.route("/blog/<id>")
def read_blog(id):
    return render_template("public/blog.html", articles=article_dict, id=id)

@app.route("/about")
def about():
    return render_template("public/about.html")

@app.route("/latest")
def latest():
    return render_template("public/latest.html", articles=article_dict)

@app.route("/contact")
def contact():
    return render_template("public/contact.html")

@app.route("/admin")
@login_required
@admin_required
def admin():
    return render_template("private/admin.html", articles=article_dict)

@app.route("/admin_login", methods=["POST", "GET"])
def admin_login():
    form = Login(request.form)
    if request.method == "POST" and form.validate():
        if validate(request.form):
            session['logged_in'] = True
            session['role'] = 'admin'  # Set the user role to admin
            return redirect(url_for('admin'))
    return render_template("private/admin_login.html", form=form)

@app.route("/new_admin", methods=['POST', 'GET'])
def new_admin():
    form = Registration(request.form)
    if request.method == "POST" and form.validate():
        article_dict['admin'] = {
            'username': form.username.data,
            'password': form.password.data
        }
        with open('articles.json', 'w') as fp:
            json.dump(article_dict, fp)
        return redirect(url_for('admin_login'))
    return render_template("private/new_admin.html", form=form)

@app.route("/admin/create_article", methods=["POST", "GET"])
@login_required
@admin_required
def create_article():
    form = Article()
    if request.method == "POST" and form.validate_on_submit():
        if 'file' not in request.files:
            return 'No file part in request'
        
        uploaded_file = request.files['file']
        
        if uploaded_file.filename == '':
            return 'No file selected'
        
        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(filepath)

            relative_filepath = "../../static/uploads/" + filename # Store relative path

            article_dict[str(uuid.uuid4())] = {
                "title": form.title.data,
                "description": form.description.data,
                "date_written": form.date,
                "text": form.article_text.data,
                "image_path": relative_filepath
            }
            with open('articles.json', 'w') as fp:
                json.dump(article_dict, fp)
            print(relative_filepath)
            return redirect(url_for('admin'))
    return render_template("private/create_article.html", form=form)

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/admin/blog/<id>")
@login_required
@admin_required
def admin_blog(id):
    return render_template("private/admin_blog.html", articles=article_dict, id=id)

@app.route("/admin/edit_blog/<id>", methods=['POST', 'GET'])
@login_required
@admin_required
def edit_blog(id):
    article = Article(request.form)
    if request.method == "POST" and article.validate():
        article_dict[id] = {
            "title": article.title.data,
            "description": article.description.data,
            "date_written": article.date,
            "text": article.article_text.data
        }
        with open('articles.json', 'w') as fp:
            json.dump(article_dict, fp)
        return redirect(url_for('admin_blog', id=id))
    else:
        article.title.data = article_dict[id]['title']
        article.description.data = article_dict[id]['description']
        article.article_text.data = article_dict[id]['text']
    return render_template("private/edit_blog.html", articles=article_dict, id=id, form=article)

@app.route("/admin/delete_blog/<id>")
@login_required
@admin_required
def delete_blog(id):
    del article_dict[id]
    with open('articles.json', 'w') as fp:
        json.dump(article_dict, fp)
    return redirect(url_for('admin'))
