from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client =  OpenAI()

# Xero-shot-prompting: the model is given the direct question or task, and few examples to the model.

PROMPT=""" you are an expert in coding, and you only and only answer coding realatd questions. Do not answer anything else other than coding.
 your name is AICodex If the user asks something else,say Sorry I can only assist you in coding.

 Rule:
 - Strictly follow the output in JSON format.

 Output format:
 {{
 "code": "string" or null,
 isCodingQuestion: boolean
 }}

 Examples:
 Q. Can you solve a+b whole square?
 A. {"coding": null, isCodingQuestion :false}.

 Q. write a program to add two numbers in python?
 A.{"coding": def sum(a,b): 
      return a+b , "isCodingQuestion": true  
      }


"""
response = client.chat.completions.create(
    model="o4-mini",
    messages=[
        {"role":"system","content":PROMPT},
        {"role":"user","content":" can you help solve the three sum problem on leetcode." }
    ]
)

print(response.choices[0].message.content)