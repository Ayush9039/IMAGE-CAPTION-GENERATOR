from flask import Flask, render_template, request
import os

app = Flask(__name__)

# -----------------------------
# Captions.txt read karne ka function
# -----------------------------
def load_captions(captions_file):
    captions_dict = {}
    try:
        with open(captions_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(None, 1)  # split at first whitespace/tab
                if len(parts) == 2:
                    image_name, caption = parts
                    captions_dict[image_name.lower()] = caption
    except FileNotFoundError:
        print(f"⚠️ Captions file '{captions_file}' not found!")
    return captions_dict

# -----------------------------
# Paths
# -----------------------------
CAPTIONS_FILE = "captions.txt"
IMAGE_FOLDER = os.path.join("static", "images")

# Folder create only if not exists
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# -----------------------------
# Captions load karo
# -----------------------------
captions_data = load_captions(CAPTIONS_FILE)
print("Loaded captions:", captions_data)  # Debug

# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def index():
    return render_template("welcome.html")  # Welcome page

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        uploaded_file = request.files.get("image")
        if uploaded_file and uploaded_file.filename != "":
            filepath = os.path.join(IMAGE_FOLDER, uploaded_file.filename)
            uploaded_file.save(filepath)

            # Caption fetch karo (lowercase match)
            caption = captions_data.get(uploaded_file.filename.lower(), "⚠️ Caption not found!")

            return render_template("result.html", image=uploaded_file.filename, caption=caption)

    return render_template("upload.html")

# -----------------------------
# Run
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)



