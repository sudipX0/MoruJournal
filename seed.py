from app import app, db
from app.models import Post, User
from datetime import datetime


def seed():
    user = User(username="admin", email="admin@example.com", password="adminpassword")
    db.session.add(user)

    post1 = Post(
        title="First Blog",
        content="This is the content of the first blog post.",
        author=user,
        date_posted=datetime.utcnow(),
    )
    post2 = Post(
        title="Second Blog",
        content="This is the content of the second blog post.",
        author=user,
        date_posted=datetime.utcnow(),
    )

    db.session.add(post1)
    db.session.add(post2)

    db.session.commit()
    print("Database seeded with initial blog posts.")
