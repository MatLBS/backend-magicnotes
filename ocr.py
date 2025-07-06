import cv2
import pytesseract
from matplotlib import pyplot as plt
import numpy as np
from utils import *

def process_image(image_path):
    img_orig = cv2.imread(image_path)
    img_thresh, img_gray = threshold_image(img_orig)
    data_ocr = image_to_data(img_thresh)

    hsv_lower = [22, 30, 30]
    hsv_upper = [45, 255, 255]

    img_mask, img_hsv = mask_image(img_orig, hsv_lower, hsv_upper)
    img_mask_denoised = denoise_image(img_mask)

    data_ocr = find_highlighted_words(img_mask_denoised, data_ocr, threshold_percentage=25)

    highlighted_text = [
        text for text, is_highlighted in zip(data_ocr['text'], data_ocr['highlighted'])
        if is_highlighted
    ]
    return normalize_highlighted_text(highlighted_text)