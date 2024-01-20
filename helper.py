import cv2

def resize_image(image, target_size):
    resized_image = cv2.resize(image, target_size)
    return resized_image