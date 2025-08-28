import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def load_posts():
    with open("posts.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_posts(posts):
    with open("posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4)


@app.route("/")
def index():
    blog_posts = load_posts()
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        posts = load_posts()

        # hole Daten aus dem Formular
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        # neue ID (einfach höchste ID + 1)
        new_id = max([post["id"] for post in posts], default=0) + 1

        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }

        # Post anhängen und speichern
        posts.append(new_post)
        save_posts(posts)

        return redirect(url_for("index"))

    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)