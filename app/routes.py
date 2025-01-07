from app import app
from flask import render_template, url_for, flash, redirect, request
from app.forms import RegistrationForm, LoginForm
from app import db, bcrypt
from app.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required

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
        hashed_password = bcrypt.generate_password_hash(reg_form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=reg_form.username.data,
            email=reg_form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created successfully !", "Success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=reg_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main"))
        else:
            flash("Invalid credentials! Please try again.", "Error")
            return render_template("login.html", title="Login", form=login_form)
    return render_template("login.html", title="Login", form=login_form)


@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main"))


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", title="Profile")
