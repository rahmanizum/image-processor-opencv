import os
from flask import current_app as app
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.image_processing.stitching import stitch_images
from app.image_processing.roi import extract_roi
from app.image_processing.zoom import zoom_roi
from app.image_processing.autofocus import auto_focus


main = Blueprint("main", __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tif', 'tiff'}
UPLOAD_FOLDER = 'temp_storage'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route("/")
def index():
    app.logger.info("Microscope Image Processor API is running!")
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

@main.route("/stitch_images", methods=["GET"])
def stitch():
    try:
        image_dir = "temp_storage"
        output_path = "temp_storage/output/stitched_output.jpg"
        result = stitch_images(image_dir, output_path)

        return jsonify({
            "message": "Images stitched successfully!",
            "stitched_image": result
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@main.route("/roi_selection", methods=["POST"])
def roi_selection():
    try:
        input_path = "temp_storage/output/stitched_output.jpg"
        output_path = "temp_storage/output/roi.jpg"

        result = extract_roi(input_path, output_path)

        return jsonify({
            "message": "ROI extracted successfully!",
            "roi_image": result["roi_path"],
            "coordinates": result["coordinates"]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@main.route("/zoom", methods=["POST"])
def zoom():
    try:
        data = request.get_json()
        zoom_level = data.get("magnification", 10)
        method = data.get("method", "bilinear")

        input_path = "temp_storage/output/roi.jpg"
        output_path = f"temp_storage/output/zoom_{zoom_level}x.jpg"

        result = zoom_roi(input_path, output_path, magnification=int(zoom_level), method=method)

        return jsonify({
            "message": f"ROI zoomed to {zoom_level}X using {method} interpolation.",
            "zoomed_image": result
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@main.route("/auto_focus", methods=["GET"])
def auto_focus_route():
    try:
        input_path = "temp_storage/output/roi.jpg" 
        output_path = "temp_storage/output/focused.jpg"

        result = auto_focus(input_path, output_path)

        return jsonify({
            "message": "Auto-focus process completed.",
            "status": result["status"],
            "laplacian_variance": result["laplacian_variance"],
            "output_image": result["focused_image"]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500