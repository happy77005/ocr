from flask import Flask, request, jsonify, render_template
from PIL import Image
import pytesseract
import os

app = Flask(__name__, template_folder="templates")

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    try:
        if "images" not in request.files:
            return jsonify({"success": False, "error": "No files uploaded"}), 400

        images = request.files.getlist("images")
        extracted_texts = []

        for image_file in images:
            try:
                image = Image.open(image_file)
                text = pytesseract.image_to_string(image)
                extracted_texts.append(text)
            except Exception as e:
                extracted_texts.append(f"Error processing image: {str(e)}")

        return jsonify({"success": True, "text": "\n\n".join(extracted_texts)})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
