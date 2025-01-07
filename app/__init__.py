from flask import Flask, render_template, url_for, redirect, flash
from config import Config
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config.from_object(Config)

posts = [
    {
        "title": "Blog Title 1",
        "author": "Author Name 1",
        "date_posted": "Date Posted 1",
        "content": "Blog Content 1",
    },
    {
        "title": "Blog Title 2",
        "author": "Author Name 2",
        "date_posted": "Date Posted 2",
        "content": "Blog Content 2",
    },
]


@app.route("/")
@app.route("/home")
def main():
    return render_template("index.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about_us.html", title="About Us")


@app.route("/register", methods=["GET", "POST"])
def register():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        flash(f"Account created successfully for {reg_form.username.data}", "Success")
        return redirect(url_for("main"))
    return render_template("register.html", title="Register", form=reg_form)


@app.route("/login")
def login():
    login_form = LoginForm()
    return render_template("login.html", title="Login", form=login_form)
