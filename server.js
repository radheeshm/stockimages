const fs = require("fs");
const path = require("path");
const express = require("express");
const multer = require("multer");
const simpleGit = require("simple-git");
require("dotenv").config();

const app = express();
const port = 3000;
const git = simpleGit();

// Ensure the images directory exists
const imagesPath = path.join(__dirname, "images");
if (!fs.existsSync(imagesPath)) {
    fs.mkdirSync(imagesPath, { recursive: true });
}

// Configure Multer to store files in the images folder with original names
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, imagesPath); // Save to 'images/' folder
    },
    filename: function (req, file, cb) {
        const ext = path.extname(file.originalname) || ".jpg"; // Ensure extension exists
        cb(null, file.fieldname + "-" + Date.now() + ext); // Add timestamp to filename
    },
});

const upload = multer({ storage: storage });

// Upload route
app.post("/upload", upload.single("image"), async (req, res) => {
    if (!req.file) {
        return res.status(400).send("❌ No file uploaded.");
    }

    try {
        // Git actions
        await git.cwd(__dirname);
        await git.add("images/*"); // Add images folder
        await git.commit(`Added ${req.file.filename}`);
        await git.push(
            `https://${process.env.GITHUB_USERNAME}:${process.env.GITHUB_PAT}@github.com/${process.env.GITHUB_USERNAME}/${process.env.GITHUB_REPO}.git`,
            "main"
        );

        res.send("✅ File uploaded and pushed to GitHub.");
    } catch (err) {
        console.error(err);
        res.status(500).send("❌ Failed to push to GitHub.");
    }
});

// Start server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
