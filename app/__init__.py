from flask import Flask, render_template, url_for

app = Flask(__name__)

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
