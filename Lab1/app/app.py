from flask import Flask, render_template

app = Flask(__name__)
application = app

@app.route("/")
def index():
    msg = "Hello"
    return render_template("index.html", message=msg)

@app.route("/posts")
def posts():
    return render_template("posts.html", message="Посты")

@app.route("/about")
def about():
    return render_template("about.html", message="Об авторе")