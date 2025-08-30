import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def load_posts():
    with open("posts.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_posts(posts):
    with open("posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4)

def fetch_post_by_id(post_id):
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            return post
    return None

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


@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = load_posts()

    # Post mit der gegebenen ID finden und entfernen
    posts = [post for post in posts if post['id'] != post_id]

    # Aktualisierte Liste speichern
    save_posts(posts)

    # Zurück zur Startseite
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = load_posts()
    post = fetch_post_by_id(post_id)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Daten aus dem Formular holen
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        # Post in der Liste finden und aktualisieren
        for i, p in enumerate(posts):
            if p['id'] == post_id:
                posts[i]['author'] = author
                posts[i]['title'] = title
                posts[i]['content'] = content
                break

        # Speichern und zurück zur Startseite
        save_posts(posts)
        return redirect(url_for('index'))

    # GET request - zeige Update-Formular
    return render_template('update.html', post=post)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
