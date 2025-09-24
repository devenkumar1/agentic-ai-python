from openai import OpenAI
from dotenv import load_dotenv
import json
from typing import List, Dict, Any
load_dotenv()

client = OpenAI()



PROMPT="""
You're an expert AI Assistant in resolving user queries using chain of thought.
You work on START, PLAN and OUTPUT steps.

You need to firstly PLAN what's need to be done. The PLAN can have multiple steps. Once you think enough PLAN has been done, finally you can give an OUTPUT.

Rules:
 - Strictly follow the given JSON output format.
 - Only give one step at a time.
 - The sequence of steps is START (where user gives an input), PLAN (that can be multiple times), and finally the OUTPUT (which is going to be displayed to the user).

OUTPUT JSON Format:
    {
    "STEP" : "START" | "PLAN" | "OUTPUT",
    "content" : "string"
    
    Example:
        START: can you solve 2+3*5/10 ?
        PLAN: step:{
        "STEP": "PLAN",
        "content": "seems like user is interested in solving a maths problem"
        },
        PLAN: step:{
        "STEP": "PLAN",
        "content": "looking at the problem we should use the BODMAS rule to solve the problem"
        },
        PLAN: step:{
        "STEP": "PLAN",
        "content": "yes, BODMAS is the correct way to solve this problem"
        },
        PLAN: step:{
        "STEP": "PLAN",
        "content": "first we need to multiply 3 with 5, that is 3*5 = 15"
        },
        PLAN: step:{
        "STEP": "PLAN",
        "content": "next, divide 15 by 10, that is 15/10 = 1.5"
        },
        PLAN: step:{
        "STEP": "PLAN",
        "content": "finally, add 2 to 1.5, that is 2 + 1.5 = 3.5"
        },
        OUTPUT: step:{
        "STEP": "OUTPUT",
        "content": "The answer is 3.5"
        }
    }  

"""
messageHistory=[{"role":"system","content":PROMPT}]
user_query = input("👉🏻")

while True:
  messageHistory.append({"role":"user","content":user_query })
  response = client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type": "json_object"},
    messages= messageHistory    # type: ignore
  )

  raw_result = response.choices[0].message.content
  if raw_result is None:
    print("❌ Error: No response from AI")
    break
    
  messageHistory.append({"role":"assistant","content":raw_result})
  try:
    parsed_result = json.loads(raw_result)
  except json.JSONDecodeError:
    print("❌ Error: Invalid JSON response")
    break
  if parsed_result.get("STEP") =="START":
    print("🔥",parsed_result.get("content"))
    user_query = "continue"   
    continue
  if parsed_result.get("STEP") =="PLAN":
    print("🧠",parsed_result.get("content"))
    user_query = "continue"  
    continue
  if parsed_result.get("STEP") =="OUTPUT":
    print("🤖",parsed_result.get("content"))
    break




# response = client.chat.completions.create(
#     model="o4-mini",
#     response_format={"type": "json_object"},
#     messages=[
#         {"role":"system","content":PROMPT},
#         {"role":"user","content":" can you help solve the three sum problem on leetcode." },
#         {"role":"assistant","content":json.dumps({"STEP": "START","content": "can you help solve the three sum problem on leetcode."}) }
#     ]
# )