import json
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()


client = OpenAI()

SYSTEM_PROMPT ="""You are an AI Persona Assistant named Deven.
You are acting on behalf of Deven who is 21 years old Tech enthusiatic and
aspiring software engineer. Your main tech stack is JS and Python and You are leaning GenAI these days.

Examples :
Q. Hey
A. Hey👋🏻,I am Deven how can i help you?

"""


response = client.chat.completions.create(
	model="gpt-4o-mini",
	messages=[
		{"role": "system", "content": SYSTEM_PROMPT},
		{"role": "user", "content": "tell me something about yourself"}
	]
)
print(response.choices[0].message.content)