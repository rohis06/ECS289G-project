import os
import openai

openai.api_key = "api-key"

def generate_visual_character(input_prompt):
    response = openai.Image.create(
        prompt=input_prompt,
        n=1,
        size="256x256",
    )

    return response["data"][0]["url"]
