from flask import current_app as app
import cv2
import numpy as np

def compute_laplacian_variance(image):
    app.logger.debug("Computing Laplacian variance")
    return cv2.Laplacian(image, cv2.CV_64F).var()

def sharpen_image(image):
    app.logger.debug("Applying sharpening filter")
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

def auto_focus(image_path, output_path, blur_threshold=100.0):
    app.logger.info(f"Starting auto-focus processing for image: {image_path}")
    
    try:
        image = cv2.imread(image_path)
        if image is None:
            app.logger.error(f"Failed to load image from {image_path}")
            return {"error": "Failed to load image"}
            
        app.logger.debug(f"Successfully loaded image from {image_path}")
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        variance = compute_laplacian_variance(gray)
        app.logger.debug(f"Calculated Laplacian variance: {variance}")
        
        if variance < blur_threshold:
            app.logger.info(f"Image is blurry (variance: {variance} < threshold: {blur_threshold}). Applying sharpening...")
            sharpened = sharpen_image(image)
            cv2.imwrite(output_path, sharpened)
            app.logger.info(f"Sharpened image saved to {output_path}")
            return {
                "focused_image": output_path,
                "status": "Sharpened (was blurry)",
                "laplacian_variance": variance
            }
        else:
            app.logger.info(f"Image is already sharp (variance: {variance} >= threshold: {blur_threshold})")
            cv2.imwrite(output_path, image)
            app.logger.info(f"Original image saved to {output_path}")
            return {
                "focused_image": output_path,
                "status": "Already sharp",
                "laplacian_variance": variance
            }
    except Exception as e:
        app.logger.error(f"Error during auto-focus processing: {str(e)}")
        raise
