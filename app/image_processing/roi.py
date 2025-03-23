from flask import current_app as app
import cv2
import os

def extract_roi(image_path, output_path):
    app.logger.info(f"Starting ROI extraction for image: {image_path}")
    
    try:
        image = cv2.imread(image_path)
        if image is None:
            app.logger.error(f"Failed to load image from {image_path}")
            return {"error": "Failed to load image"}
            
        app.logger.debug(f"Successfully loaded image from {image_path}")
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        app.logger.debug("Converted image to grayscale")

        # Threshold to segment objects
        app.logger.debug("Applying threshold to segment objects")
        _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Find contours
        app.logger.debug("Finding contours in the image")
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            app.logger.error("No contours found in the image")
            raise ValueError("No contours found in the image.")

        # Choose the largest contour
        app.logger.debug(f"Found {len(contours)} contours, selecting the largest")
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        app.logger.info(f"ROI bounding box: x={x}, y={y}, width={w}, height={h}")

        # Extract ROI
        roi = image[y:y+h, x:x+w]
        cv2.imwrite(output_path, roi)
        app.logger.info(f"ROI successfully extracted and saved to {output_path}")

        return {
            "roi_path": output_path,
            "coordinates": {"x": x, "y": y, "width": w, "height": h}
        }
    except ValueError as ve:
        app.logger.error(f"ValueError during ROI extraction: {str(ve)}")
        raise
    except Exception as e:
        app.logger.error(f"Error during ROI extraction: {str(e)}")
        raise
