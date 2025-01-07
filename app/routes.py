from app import app
from flask import abort, render_template, url_for, flash, redirect, request
from app.forms import RegistrationForm, LoginForm, UpdateProfile, PostForm
from app import db, bcrypt
from app.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os


@app.route("/")
@app.route("/home")
def main():
    post = Post.query.all()
    return render_template("index.html", posts=post)


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


def update_picture(upd_form_picture):
    file_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(upd_form_picture.filename)
    picture_fn = file_hex + file_ext
    picture_path = os.path.join(app.root_path, "static/images", picture_fn)
    upd_form_picture.save(picture_path)
    return picture_fn


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    upd_form = UpdateProfile()
    if upd_form.validate_on_submit():
        if upd_form.picture.data:
            picture_file = update_picture(upd_form.picture.data)
            current_user.image_file = picture_file
        current_user.username = upd_form.username.data
        current_user.email = upd_form.email.data
        db.session.commit()
        flash("Account Updated !", "Success")
        return redirect(url_for("profile"))
    elif request.method == "GET":
        upd_form.username.data = current_user.username
        upd_form.email.data = current_user.email
    image_file = url_for("static", filename="images/" + current_user.image_file)
    return render_template(
        "profile.html", title="Profile", image_file=image_file, form=upd_form
    )


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    post_form = PostForm()
    if post_form.validate_on_submit():
        post = Post(
            title=post_form.title.data,
            content=post_form.content.data,
            author=current_user,
        )
        db.session.add(post)
        db.session.commit()
        flash("Post Created !", "Success")
        return redirect(url_for("main"))
    return render_template(
        "create_post.html", title="New Post", form=post_form, legend="New Post"
    )


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    update_post_form = PostForm()

    if update_post_form.validate_on_submit():
        post.title = update_post_form.title.data
        post.content = update_post_form.content.data
        db.session.commit()
        flash("Post updated successfully!", "Success")
        return redirect(url_for("post", post_id=post.post_id))

    elif request.method == "GET":
        update_post_form.title.data = post.title
        update_post_form.content.data = post.content

    return render_template(
        "create_post.html",
        title="Update Post",
        form=update_post_form,
        legend="Update Post",
    )


@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash("Post Deleted!", "Success")
    return redirect(url_for("main"))
