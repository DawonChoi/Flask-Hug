from app import app
from datetime import datetime

from flask import render_template
from flask import request, redirect
from flask import jsonify, make_response
from werkzeug.utils import secure_filename

import os

#configuration image
app.config["IMAGE_UPLOADS"] = "C:/flask-Hug/app/static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024

#configuration audio
app.config["AUDIO_UPLOADS"] = "C:/flask-Hug/app/static/audio/uploads"
app.config["ALLOWED_AUDIO_EXTENSIONS"] = ["MP3", "WAV", "WMA", "AIFF", "ALAC"]


# hard coding
users = {
    "dawon": {
        "name": "Dawon Choi",
        "bio": "CTO, Google LLC",
        "twitter_handle": "@dawon"
    }
}


def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:
            if "filesize" in request.cookies:
                if not allowed_image_filesize(request.cookies["filesize"]):
                    print("Filesize exceeded maximum limit")
                    return redirect(request.url)

                image = request.files["image"]

                if image.filename == "":
                    print("No filename")
                    return redirect(request.url)
                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    print("Image saved")
                    return redirect(request.url)
                else:
                    print("That file extension is not allowed")
                    return redirect(request.url)

    return render_template("public/upload.html")


@app.route("/upload-audio", methods=["GET", "POST"])
def upload_image():
    return render_template("public/upload.html")






@app.route("/")
def index():
    return render_template("public/index.html")


@app.route("/about")
def about():
    return """
    <h1 style='color: red;'>I'm a red H1 heading!</h1>
    <p>This is a lovely little paragraph</p>
    <code>Flask is <em>awesome</em></code>
    """


@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")


@app.route("/sign-up", methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        req = request.form
        password = req["password"]
        conf_password = req["conf_password"]

        print(password+' '+conf_password)
        # empty list -> full list has members of number of error
        missing = list()

        for key, value in req.items():
            if value == "":
                missing.append(key)

        # 1. check a empty field 2.checking mismatched case of password confirmation
        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template("public/sign_up.html", feedback=feedback)
        elif password != conf_password:
             feedback = "Password mismatch"
             return render_template("public/sign_up.html", feedback=feedback)
        else:
            success = "Success!!!"
            return render_template("public/sign_up.html", success=success)

    return render_template("public/sign_up.html")


@app.route("/json", methods=["POST"])
def json_example():
    if request.is_json:
        req = request.get_json()
        response_body = {
            "message": "JSON received!",
            "sender": req.get("name")
        }
        res = make_response(jsonify(response_body), 200)
        return res
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)


@app.route("/query")
def query():
    if request.args:
        args = request.args
        serialized = ", ".join(f"{k}: {v}" for k, v in request.args.items())
        return f"(Query) {serialized}", 200
    else:
        return "No query string received", 200 


@app.route("/guestbook")
def guestbook():
    return render_template("public/guestbook.html")


@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():
    req = request.get_json()
    print(req)
    res = make_response(jsonify(req), 200)
    return res


@app.route("/profile")
def profile_page():
    return render_template("public/profile.html")


@app.route("/profile/<username>")
def profile(username):
    user = None

    if username in users:
        user = users[username]

    return render_template("public/profile.html", username=username, user=user)


@app.route("/jinja")
def jinja():
    # Strings
    my_name = "Dawon"

    # Integers
    my_age = 18

    # Lists
    langs = ["Python", "JavaScript", "Bash", "Ruby", "C", "Rust"]

    # Dictionaries
    friends = {
        "Tony": 43,
        "Cody": 28,
        "Amy": 26,
        "Clarissa": 23,
        "Wendell": 39
    }

    # Tuples
    colors = ("Red", "Blue")

    # Booleans
    cool = True

    # Classes
    class GitRemote:
        def __init__(self, name, description, domain):
            self.name = name
            self.description = description 
            self.domain = domain

        def pull(self):
            return f"Pulling repo '{self.name}'"

        def clone(self, repo):
            return f"Cloning into {repo}"

    my_remote = GitRemote(
        name="flask-Hug",
        description="flask web server that provide file uploading but main offering is .mp3",
        domain="https://github.com/DawonChoi/Flask-Hug.git"
    )

    # Functions
    def repeat(x, qty=1):
        return x * qty

    date = datetime.utcnow()

    return render_template(
        "public/jinja.html", my_name=my_name, my_age=my_age, langs=langs,
        friends=friends, colors=colors, cool=cool, GitRemote=GitRemote, 
        my_remote=my_remote, repeat=repeat, date=date
    )