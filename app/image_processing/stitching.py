from flask import current_app as app
import cv2
import os
import numpy as np

def stitch_images(image_dir, output_path):
    image_files = sorted([
        f for f in os.listdir(image_dir)
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.tif', '.tiff'))
    ])

    if len(image_files) < 2:
        raise ValueError("Need at least 2 images to perform stitching.")

    # Load images
    images = [cv2.imread(os.path.join(image_dir, f)) for f in image_files]

    # ORB detector
    orb = cv2.ORB_create(nfeatures=2000)

    stitched_image = images[0]

    for i in range(1, len(images)):
        kp1, des1 = orb.detectAndCompute(stitched_image, None)
        kp2, des2 = orb.detectAndCompute(images[i], None)

        # Brute Force Matcher
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)

        if len(matches) < 10:
            raise ValueError("Not enough matches between images.")

        # Extract location of good matches
        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1,1,2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1,1,2)

        # Homography
        H, _ = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)

        # Warp and stitch
        height, width = stitched_image.shape[:2]
        warped = cv2.warpPerspective(images[i], H, (width + images[i].shape[1], height))
        warped[0:height, 0:width] = stitched_image

        stitched_image = warped

    # Crop black borders (optional)
    gray = cv2.cvtColor(stitched_image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(contours[0])
    cropped = stitched_image[y:y+h, x:x+w]

    # Save result
    cv2.imwrite(output_path, cropped)

    return output_path
