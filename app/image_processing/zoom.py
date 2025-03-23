from flask import current_app as app
import cv2

def zoom_roi(image_path, output_path, magnification=10, method="bilinear"):
    if magnification not in [10, 20]:
        raise ValueError("Only 10X and 20X zoom levels are supported.")

    image = cv2.imread(image_path)

    zoom_factor = magnification // 10  # 10X -> 1, 20X -> 2
    width = image.shape[1] * zoom_factor
    height = image.shape[0] * zoom_factor

    interpolation = {
        "bilinear": cv2.INTER_LINEAR,
        "bicubic": cv2.INTER_CUBIC
    }.get(method.lower(), cv2.INTER_LINEAR)

    zoomed = cv2.resize(image, (width, height), interpolation=interpolation)
    cv2.imwrite(output_path, zoomed)

    return output_path
