from app import app
from flask import abort, render_template, url_for, flash, redirect, request
from app.forms import (
    RegistrationForm,
    LoginForm,
    UpdateProfile,
    PostForm,
    RequestResetForm,
    ResetPasswordForm,
)
from app import db, bcrypt, mail
from app.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from flask_mail import Message


@app.route("/")
@app.route("/home")
def main():
    page = request.args.get("page", default=1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
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
    flash("Logged Out Successfully !", "Success")
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


@app.route("/my_blogs")
@login_required
def my_blogs():
    # Fetch all blogs created by the current user
    posts = (
        Post.query.filter_by(author=current_user)
        .order_by(Post.date_posted.desc())
        .all()
    )
    return render_template("my_blogs.html", posts=posts)


@app.route("/user/<string:username>")
def user_blogs(username):
    # Query the user by username
    user = User.query.filter_by(username=username).first_or_404()

    # Fetch all posts by this user
    page = request.args.get("page", 1, type=int)
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=5)
    )

    return render_template("user_blogs.html", posts=posts, user=user)


# Commented out the email sending part for local testing
# def send_reset_email(user):
#     token = user.get_reset_token()
#     msg = Message(
#         "Reset Password Request",
#         sender="noreply@morujournal.com",
#         recipients=[user.email],
#     )
#     msg.body = f"""Vist the following link:
#     {url_for('reset_token', token=token, _external=True)}
#     Safely disregard this mail if you didn't request to reset your password.
# """
#     mail.send(message=msg)


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # For local testing, just render success message without email
        flash(
            "An email has been sent with instructions to reset your password.",
            "Success",
        )
        return redirect(url_for("login"))

    return render_template("reset_request.html", title="Reset Password", form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Invalid Token!", "Error")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Update password logic (just for testing, don't hash here for now)
        hashed_password = form.password.data  # For testing purposes, skip hashing
        user.password = hashed_password
        db.session.commit()
        flash(f"Password Updated successfully !", "Success")
        return redirect(url_for("login"))

    return render_template("reset_token.html", title="Reset Password", form=form)
