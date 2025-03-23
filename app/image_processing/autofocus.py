import cv2
import numpy as np

def compute_laplacian_variance(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

def sharpen_image(image):
    # Simple sharpening kernel
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

def auto_focus(image_path, output_path, blur_threshold=100.0):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    variance = compute_laplacian_variance(gray)

    if variance < blur_threshold:
        sharpened = sharpen_image(image)
        cv2.imwrite(output_path, sharpened)
        return {
            "focused_image": output_path,
            "status": "Sharpened (was blurry)",
            "laplacian_variance": variance
        }
    else:
        cv2.imwrite(output_path, image)
        return {
            "focused_image": output_path,
            "status": "Already sharp",
            "laplacian_variance": variance
        }
