from blog_app import app
from flask import render_template
from flask import url_for

@app.route("/")
def index():
    print("Hello")
    return render_template("public/index.html")

@app.route("/blog")
def blog():
    return render_template("public/blog.html")

@app.route("/about")
def about():
    return render_template("public/about.html")

@app.route("/latest")
def latest():
    return render_template("public/latest.html")