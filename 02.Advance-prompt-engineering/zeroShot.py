from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client =  OpenAI()

# Xero-shot-prompting: the model is given the direct question or task, without any prior examples.

PROMPT="you are an expert in coding, and you only and only answer coding realatd questions. Do not answer anything else other than coding. your name is AICodex If the user asks something else,say Sorry I can only assist you in coding"
response = client.chat.completions.create(
    model="o4-mini",
    messages=[
        {"role":"system","content":PROMPT},
        {"role":"user","content":" a^2 + b^2=?" }
    ]
)

print(response.choices[0].message.content)