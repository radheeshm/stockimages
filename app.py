import os
from flask import Flask, render_template, request, redirect, url_for
from github import Github
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "static/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# GitHub Credentials
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
GITHUB_REPO = "radheeshm/stockimages"

# Initialize GitHub API
g = Github(GITHUB_ACCESS_TOKEN)
repo = g.get_repo(GITHUB_REPO)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            # Upload image to GitHub
            with open(filepath, "rb") as f:
                content = f.read()
                repo.create_file(f"uploads/{file.filename}", f"Add {file.filename}", content, branch="main")
            
            return redirect(url_for("upload_file"))

    # Fetch images from GitHub repository
    images = []
    contents = repo.get_contents("uploads")
    for file in contents:
        images.append(file.download_url)

    return render_template("index.html", images=images)

if __name__ == "__main__":
    app.run(debug=True)
