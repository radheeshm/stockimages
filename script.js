const GITHUB_USERNAME = "radheeshm";
const REPO_NAME = "stockimages";
const BRANCH = "main"; // or "master" if default
const ACCESS_TOKEN = "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";

async function uploadImage() {
    const fileInput = document.getElementById("fileInput");
    if (!fileInput.files.length) {
        alert("Please select a file first!");
        return;
    }

    const file = fileInput.files[0];
    const reader = new FileReader();
    
    reader.onload = async function () {
        const content = reader.result.split(",")[1]; // Remove data URI prefix

        const path = `uploads/${file.name}`;
        const url = `https://api.github.com/repos/${GITHUB_USERNAME}/${REPO_NAME}/contents/${path}`;
        
        const response = await fetch(url, {
            method: "PUT",
            headers: {
                "Authorization": `token ${ACCESS_TOKEN}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: `Upload ${file.name}`,
                content: content,
                branch: BRANCH
            })
        });

        if (response.ok) {
            document.getElementById("status").innerText = "✅ Image uploaded successfully!";
        } else {
            document.getElementById("status").innerText = "❌ Upload failed!";
        }
    };
    
    reader.readAsDataURL(file);
}

