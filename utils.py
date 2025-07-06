import cv2
import numpy as np
import pytesseract
from pytesseract import Output


def threshold_image(img_src):
	"""Grayscale image and apply Otsu's threshold"""
	# Grayscale
	img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
	# Binarisation and Otsu's threshold
	_, img_thresh = cv2.threshold(
		img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

	return img_thresh, img_gray


def image_to_data(img_src):
	return pytesseract.image_to_data(
		img_src, lang='eng', config='--psm 6', output_type=Output.DICT)


def extract_all(img_src, img_thresh):
	# Extract all text as one string
	string_ocr = pytesseract.image_to_string(
		img_thresh, lang='eng', config='--psm 6')
	# Extract all text and meta data as dictionary
	data_ocr = pytesseract.image_to_data(
		img_src, lang='eng', config='--psm 6', output_type=Output.DICT)
	# Copy source image to draw rectangles
	img_result = img_src.copy()

	# Iterate through all words
	for i in range(len(data_ocr['text'])):
		# Skip other levels than 5 (word)
		# Level 5 corresponds to word level in pytesseract's output
		if data_ocr['level'][i] != 5: 
			continue
		# Get bounding box position and size of word
		(x, y, w, h) = (data_ocr['left'][i], data_ocr['top']
						[i], data_ocr['width'][i], data_ocr['height'][i])
		# Draw rectangle for word bounding box
		cv2.rectangle(img_result, (x, y), (x + w, y + h), (0,0,255), 2)

	return img_result


def mask_image(img_src, lower, upper):
	"""Convert image from RGB to HSV and create a mask for given lower and upper boundaries."""
	# RGB to HSV color space conversion
	img_hsv = cv2.cvtColor(img_src, cv2.COLOR_BGR2HSV)
	hsv_lower = np.array(lower, np.uint8)  # Lower HSV value
	hsv_upper = np.array(upper, np.uint8)  # Upper HSV value

	# Color segmentation with lower and upper threshold ranges to obtain a binary image
	img_mask = cv2.inRange(img_hsv, hsv_lower, hsv_upper)

	return img_mask, img_hsv


def denoise_image(img_src):
	"""Denoise image with a morphological transformation."""

	# Morphological transformations to remove small noise
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
	img_denoised = cv2.morphologyEx(
		img_src, cv2.MORPH_OPEN, kernel, iterations=1)

	return img_denoised


def apply_mask(img_src, img_mask):
	"""Apply bitwise conjunction of source image and image mask."""

	img_result = cv2.bitwise_and(img_src, img_src, mask=img_mask)

	return img_result


def find_highlighted_words(img_mask, data_ocr, threshold_percentage=25):
	"""Find highlighted words by calculating how much of the words area contains white pixels compared to balack pixels."""

	# Initiliaze new column for highlight indicator
	data_ocr['highlighted'] = [False] * len(data_ocr['text'])

	for i in range(len(data_ocr['text'])):
		# Get bounding box position and size of word
		(x, y, w, h) = (data_ocr['left'][i], data_ocr['top']
						[i], data_ocr['width'][i], data_ocr['height'][i])
		# Calculate threshold number of pixels for the area of the bounding box
		rect_threshold = (w * h * threshold_percentage) / 100
		# Select region of interest from image mask
		img_roi = img_mask[y:y+h, x:x+w]
		# Count white pixels in ROI
		count = cv2.countNonZero(img_roi)
		# Set word as highlighted if its white pixels exceeds the threshold value
		if count > rect_threshold:
			data_ocr['highlighted'][i] = True

	return data_ocr


def normalize_highlighted_text(text_list):
	# Étape 1: Supprimer les entrées vides
	cleaned = [word for word in text_list if word.strip()]
		
	# Étape 2: Réunir les mots séparés par '-'
	normalized = []
	i = 0
	while i < len(cleaned):
		current_word = cleaned[i]
		
		# Si le mot se termine par '-', chercher le mot suivant
		if current_word.endswith('-'):
			if i + 1 < len(cleaned):
				# Enlever le '-' et joindre avec le mot suivant
				combined_word = current_word[:-1] + cleaned[i + 1]
				normalized.append(combined_word)
				i += 2  # Sauter le mot suivant car il a été combiné
			else:
				# Si c'est le dernier mot, garder tel quel
				normalized.append(current_word)
				i += 1
		else:
			normalized.append(current_word)
			i += 1

	return normalized