import base64
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def process_image(base64_image):
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
	print( response.output_text)
	return response.output_text

def process_summary(notes):
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
