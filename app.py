import os
import requests
import base64
from flask import Flask, request, render_template
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = "radheeshm/stockimages"  # Replace with your repository

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            filename = file.filename
            file_path = f"images/{filename}"
            file.save(file_path)
            upload_to_github(file_path, filename)
            return "Image uploaded successfully!"

    return '''
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="image">
            <input type="submit" value="Upload">
        </form>
    '''

def upload_to_github(file_path, filename):
    """Uploads image to GitHub repository."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/images/{filename}"
    
    with open(file_path, "rb") as file:
        content = base64.b64encode(file.read()).decode("utf-8")  # Encode in base64

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "message": f"Upload {filename}",
        "content": content
    }

    response = requests.put(url, json=data, headers=headers)
    
    if response.status_code == 201:
        print("Upload successful!")
    else:
        print("Error:", response.json())

if __name__ == "__main__":
    app.run(debug=True)
