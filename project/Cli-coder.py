
from openai import OpenAI
import os
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv
import json
import subprocess

load_dotenv()

client = OpenAI()

def run_command(cmd: str) -> str:
    """Execute a shell command and capture both output and errors"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            output = result.stdout.strip() if result.stdout.strip() else "Command executed successfully"
            return f"✅ {output}"
        else:
            error = result.stderr.strip() if result.stderr.strip() else f"Command failed with exit code {result.returncode}"
            return f"❌ {error}"
    except Exception as e:
        return f"❌ Error executing command: {str(e)}"

def create_file_with_content(filepath: str, content: str) -> str:
    """Create a file with the specified content, handling encoding and special characters properly"""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Write content to file with proper encoding
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"✅ File '{filepath}' created successfully with {len(content)} characters"
    except Exception as e:
        return f"❌ Error creating file: {str(e)}"

def append_to_file(filepath: str, content: str) -> str:
    """Append content to an existing file"""
    try:
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(content)
        return f"✅ Content appended to '{filepath}' successfully"
    except Exception as e:
        return f"❌ Error appending to file: {str(e)}"

class ResultOutputFormat(BaseModel):
  STEP: str = Field(..., description="The ID of the step. Example: START | PLAN | TOOL | OUTPUT")
  content: Optional[str] = Field(..., description="The optional str content of the step.")
  tool: Optional[str] = Field(None, description="the ID of the Tool to call")
  input: Optional[str] = Field(None, description="the input params for the tool")
  filepath: Optional[str] = Field(None, description="File path for create_file and append_file tools")
  file_content: Optional[str] = Field(None, description="File content for create_file and append_file tools")

SYSTEM_PROMPT = """
You're an expert AI coding assistant that can execute Linux/Windows commands on the user's system to create any coding project they request.
You work through START, PLAN, TOOL, and OUTPUT steps to resolve user queries systematically.

WORKFLOW:
1. START: Acknowledge the user's request
2. PLAN: Break down the task into logical steps (can be multiple PLAN steps)
3. TOOL: Execute necessary commands/tools to complete the task (can be multiple TOOL steps)
4. OUTPUT: Provide the final result or summary to the user

Available Tools:
- run_command: Execute Linux/Windows commands on the user's system to create folders, run code, install packages, etc.
  Usage: {"STEP": "TOOL", "tool": "run_command", "input": "command_to_execute", "content": "Description of what this command does"}

- create_file: Create a new file with specific content (PREFERRED for file creation with content)
  Usage: {"STEP": "TOOL", "tool": "create_file", "filepath": "path/to/file.ext", "file_content": "complete file content here", "content": "Description of what this file does"}

- append_file: Append content to an existing file
  Usage: {"STEP": "TOOL", "tool": "append_file", "filepath": "path/to/file.ext", "file_content": "content to append", "content": "Description of what you're appending"}

IMPORTANT ERROR HANDLING RULES:
- If a command fails, READ the error message carefully and adapt accordingly
- Common scenarios to handle gracefully:
  * "already exists" errors → Skip and continue with next logical step
  * "file not found" → Create the missing file/directory first
  * "permission denied" → Try alternative approaches
  * "command not found" → Use alternative commands or inform user
- NEVER stop the entire process due to recoverable errors
- Use error information to make intelligent decisions for next steps
- Always work towards completing the user's goal even if some commands fail
- If a directory already exists, simply proceed to create files inside it

Rules:
 - Strictly follow the given JSON output format.
 - Only give one step at a time.
 - For creating files with content, ALWAYS use create_file tool instead of echo commands
 - For appending to files, use append_file tool instead of echo >>
 - Use run_command only for system operations like creating directories, installing packages, running programs
 - Always explain what each command does in the content field.
 - The sequence is: START → PLAN(s) → TOOL(s) → OUTPUT
 - CONTINUE WORKING even if some commands fail - adapt based on error messages

IMPORTANT FILE CREATION GUIDELINES:
- NEVER use echo commands for file creation with content
- ALWAYS use create_file tool for creating files with HTML, JavaScript, Python, or any code content
- Use proper file paths (forward slashes work on both Windows and Linux)
- Include complete, properly formatted content in file_content field

OUTPUT JSON Format:
{
    "STEP": "START" | "PLAN" | "TOOL" | "OUTPUT",
    "content": "Description of what you're doing",
    "tool": "tool_name (only for TOOL steps)",
    "input": "tool_parameters (only for TOOL steps)"
}

Example for a coding task:
User: "Create a simple Python calculator"

START: {"STEP": "START", "content": "I'll help you create a simple Python calculator application."}

PLAN: {"STEP": "PLAN", "content": "I need to create a Python file with basic calculator functions (add, subtract, multiply, divide) and a user interface."}

PLAN: {"STEP": "PLAN", "content": "The calculator should handle user input, perform operations, and display results with error handling."}

TOOL: {"STEP": "TOOL", "tool": "create_file", "filepath": "calculator.py", "file_content": "def add(x, y):\n    return x + y\n\ndef subtract(x, y):\n    return x - y\n\ndef multiply(x, y):\n    return x * y\n\ndef divide(x, y):\n    if y != 0:\n        return x / y\n    else:\n        return 'Error: Division by zero'\n\nprint('Simple Calculator')\nprint('Operations: +, -, *, /')\nnum1 = float(input('Enter first number: '))\nop = input('Enter operator: ')\nnum2 = float(input('Enter second number: '))\n\nif op == '+':\n    result = add(num1, num2)\nelif op == '-':\n    result = subtract(num1, num2)\nelif op == '*':\n    result = multiply(num1, num2)\nelif op == '/':\n    result = divide(num1, num2)\nelse:\n    result = 'Invalid operator'\n\nprint(f'Result: {result}')", "content": "Creating calculator.py with complete calculator functionality"}

OUTPUT: {"STEP": "OUTPUT", "content": "Calculator created successfully! The calculator.py file includes addition, subtraction, multiplication, and division functions with a user-friendly interface and error handling. You can run it with 'python calculator.py'."}
"""

messageHistory = []
messageHistory.append({"role": "system", "content": SYSTEM_PROMPT})
userInput = input("👉 ")
messageHistory.append({"role": "user", "content": userInput})

while True:
  response = client.chat.completions.parse(
    model="gpt-4o",
    messages=messageHistory,
    response_format=ResultOutputFormat
  )
  raw_content = response.choices[0].message.parsed
  if raw_content is None:
    print("Error: No response content from OpenAI.")
    break

  messageHistory.append({"role": "assistant", "content": str(raw_content)})

  if raw_content.STEP == "START":
    print("🔥", raw_content.content)
    continue
  elif raw_content.STEP == "PLAN":
    print("🧠", raw_content.content)
    continue
  elif raw_content.STEP == "TOOL":
    print("🔧", raw_content.content)
    if raw_content.tool == "run_command" and raw_content.input:
      print(f"   Executing: {raw_content.input}")
      tool_output = run_command(raw_content.input)
      print(f"   {tool_output}")
      messageHistory.append({"role": "user", "content": f"Tool output: {tool_output}"})
    elif raw_content.tool == "create_file" and raw_content.filepath and raw_content.file_content:
      print(f"   Creating file: {raw_content.filepath}")
      tool_output = create_file_with_content(raw_content.filepath, raw_content.file_content)
      print(f"   {tool_output}")
      messageHistory.append({"role": "user", "content": f"Tool output: {tool_output}"})
    elif raw_content.tool == "append_file" and raw_content.filepath and raw_content.file_content:
      print(f"   Appending to file: {raw_content.filepath}")
      tool_output = append_to_file(raw_content.filepath, raw_content.file_content)
      print(f"   {tool_output}")
      messageHistory.append({"role": "user", "content": f"Tool output: {tool_output}"})
    continue
  elif raw_content.STEP == "OUTPUT":
    print("🤖", raw_content.content)
    break
