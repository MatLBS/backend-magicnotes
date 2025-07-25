import cv2
from matplotlib import pyplot as plt
import numpy as np
from utils import *
import base64
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def process_image(image_path):
    # img_orig = cv2.imread(image_path)
    
    # img_thresh, img_gray = threshold_image(img_orig)
    # data_ocr = image_to_data(img_thresh)

    # hsv_lower = [22, 30, 30]
    # hsv_upper = [45, 255, 255]

    # img_mask, img_hsv = mask_image(img_orig, hsv_lower, hsv_upper)
    # img_mask_denoised = denoise_image(img_mask)

    # data_ocr = find_highlighted_words(img_mask_denoised, data_ocr, threshold_percentage=25)

    # highlighted_text = [
    #     text for text, is_highlighted in zip(data_ocr['text'], data_ocr['highlighted'])
    #     if is_highlighted
    # ]
    # return normalize_highlighted_text(highlighted_text)

	# Getting the Base64 string
	base64_image = encode_image(image_path)


	response = client.responses.create(
		model="gpt-4.1-mini",
		input=[
			{
				"role": "user",
				"content": [
					{ "type": "input_text", "text": "Here is an image of a page. Please list all the words that are highlighted, regardless of the color. Give only the highlighted words without any additional explanation." },
					{
						"type": "input_image",
						"image_url": f"data:image/jpeg;base64,{base64_image}",
					},
				],
			}
		],
	)

	return response.output_text

def process_summary(notes):
	print(notes)
	response = client.responses.create(
		model="gpt-4.1-mini",
		input=[
			{
				"role": "user",
				"content": [
					{ "type": "input_text", "text": "Summarize the following notes. Please write the summary in the same language as the original notes." },
					{
						"type": "input_text",
						"text": notes,
					},
				],
			}
		],
	)
	return response.output_text