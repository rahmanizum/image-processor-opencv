import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

main = Blueprint("main", __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tif', 'tiff'}
UPLOAD_FOLDER = 'temp_storage'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route("/")
def index():
    return "Microscope Image Processor API is running!"

@main.route("/upload_images", methods=["POST"])
def upload_images():
    if 'images' not in request.files:
        return jsonify({"error": "No image files part in the request"}), 400

    files = request.files.getlist('images')
    saved_files = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)
            saved_files.append(filename)
        else:
            return jsonify({"error": f"File {file.filename} is not a valid image format."}), 400

    return jsonify({
        "message": f"{len(saved_files)} image(s) uploaded successfully.",
        "files": saved_files
    }), 200
