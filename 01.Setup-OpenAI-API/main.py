from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client =  OpenAI()

response = client.chat.completions.create(
    model="o4-mini",
    messages=[
        {"role":"user","content":"hey there" }
    ]
)

print(response.choices[0].message.content)