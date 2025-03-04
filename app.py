import os
import time
from flask import Flask, render_template, request, redirect, url_for
from github import Github
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Upload folder for temporary storage
UPLOAD_FOLDER = "static/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# GitHub Credentials
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
GITHUB_REPO = "radheeshm/stockimages"

# Initialize GitHub API
if not GITHUB_ACCESS_TOKEN:
    raise ValueError("GitHub Access Token is missing!")

g = Github(GITHUB_ACCESS_TOKEN)
repo = g.get_repo(GITHUB_REPO)

# Cache GitHub images to reduce API calls
cached_contents = None
last_fetch_time = 0


@app.route("/", methods=["GET", "POST"])
def upload_file():
    global cached_contents, last_fetch_time

    if request.method == "POST":
        file = request.files["file"]
        if not file or file.filename == "":
            return "No selected file"

        # Save file locally
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        # Upload image to GitHub
        with open(filepath, "rb") as f:
            content = f.read()
            repo.create_file(f"images/{file.filename}", f"Add {file.filename}", content, branch="main")

        return redirect(url_for("upload_file"))

    # Fetch images from GitHub (limit API calls)
    if time.time() - last_fetch_time > 60:  # Only fetch once per minute
        try:
            cached_contents = repo.get_contents("uploads")
            last_fetch_time = time.time()
        except Exception as e:
            print("GitHub Error:", e)
            cached_contents = []

    images = [file.download_url for file in cached_contents] if cached_contents else []

    return render_template("index.html", images=images)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
