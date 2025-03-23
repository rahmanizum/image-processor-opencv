import cv2
import os

def extract_roi(image_path, output_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold to segment objects
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        raise ValueError("No contours found in the image.")

    # Choose the largest contour
    largest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest)

    # Extract ROI
    roi = image[y:y+h, x:x+w]
    cv2.imwrite(output_path, roi)

    return {
        "roi_path": output_path,
        "coordinates": {"x": x, "y": y, "width": w, "height": h}
    }
