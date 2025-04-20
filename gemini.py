import json
import requests
from dotenv import load_dotenv

from google import genai
from google.genai import types
import os
import typing_extensions as typing
import subprocess
load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def query_db(sql):
    pass

def write_file(file_name, content):
    try:
        # Ensure directory exists
        directory = os.path.dirname(file_name)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        # Write to file
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {file_name}"
    except Exception as e:
        return f"An error occurred while writing to the file: {e}"
def run_command(command):
    result=os.system(command=command)
    return result

def folder_create(path: str):
    newpath = f'{path}' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)


avaiable_tools = {

    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns ouput"
    },
   "write_file": {
        "fn": write_file,
        "description": "takes the filename and the content and writes in it"
    }
}

system_prompt = system_prompt = f"""
    You are an helpful AI coding Assistant who is specialized in writing and debbugging code.You are on Windows Operating System and use terminal commands accordingly
    You work on start, plan, action, observe mode.
    For given user query and using only tools listed,you must:
    1.Understand the task (start & plan phase)
    2.Break it into small steps,decide what to do first.
    3.Choose the appropriate tool from the available list.
    4.Call one tool at a time using action.
    5. Wait for and interpret the result in observe step.
    6. Continue until the task is complete,then responmd with a final `output`.

    Rules:
    - IMPORTANT:You must return ONE step at a time and wait for the observation result before proceeding to the next step.Never return multiple steps in a single response.
    - Follow the Output JSON Format.
    -  Always perform one step at a time and wait for next input
    - Carefully analyse the user query
    

    Output JSON Format:
    {{{{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}}}

    Available Tools:
    - get_weather: Takes a city name as an input and returns the current weather for the city
    - run_command: Takes a command as input to execute on system and returns ouput
    - write_file: Takes an object with filename and content fields as input. Example: {{"filename": "sum.py", "content": "print('Hello')"}}
    
    Example:
    user_query="create a simple express server"
    Output:{{"step":"plan","content":"user wants to create a basic express server"}}
    Output:{{"step":"plan","content":"use the available tools to create the necessary files or folders "}}
    Output:{{"step":"action","function":"run_command",input:"my-project"}}
    Output:{{"step":"observe","content":"structure created"}}
    Output:{{"step":"output","content":"express server created"}}

    How to use Tool write_file

    your action step should be like
    Output:{{"step":"action","function":"write file","input":""file_name.txt","content""]}}
    


"""
print("Hey! whatsup I am your coding assistant ready to code")
messages = [
    types.Content( role ="assistant", parts=[types.Part.from_text(text=system_prompt )])
]

while True:
    user_query = input('> ')
    messages.append(types.Content(role ="user", parts=[types.Part.from_text(text= user_query)]))

    while True:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
                
            ),
            contents=messages
        )
        response_text = response.text
        print("before", response_text)
        parsed_output = json.loads(response_text)
        print("after", parsed_output)

        if isinstance(parsed_output,list):
            for item in parsed_output:
                step=item.get("step")
            
            if step=="plan":
                print(f"🧠: {item.get('content')}")
            elif step=="action":
                tool_name=item.get("function")
                tool_input = item.get("input")
                if tool_name == "write_file":
                    if isinstance(tool_input, str):
                        tool_input = json.loads(tool_input)
                    if "filename" in tool_input:
                        file_name=tool_input["filename"]
                    elif "file_to_write" in tool_input:
                        file_name=tool_input["file_to_write"]
                    else:
                        print("Error: Missing filename in write_file input")
                        file_name="output.txt"
                    content=tool_input["content"]
                    output=avaiable_tools[tool_name]["fn"](file_name,content)
                else:
                     output = avaiable_tools[tool_name]["fn"](tool_input)
            elif step == "output":
                print(f"🤖: {item.get('content')}")

                break
                

            messages.append(types.Content(role= "assistant", parts=[types.Part.from_text(text= response_text)] ))
            break
        else:
             messages.append(types.Content(role="assistant", parts=[types.Part.from_text(text=response_text)]))

             if parsed_output.get("step") == "plan":
                print(f"🧠: {parsed_output.get('content')}")
                continue

             if parsed_output.get("step") == "action":
                tool_name = parsed_output.get("function")
                tool_input = parsed_output.get("input")
                if tool_name == "write_file":
                     if isinstance(tool_input, str):
                        tool_input = json.loads(tool_input)
                     if "filename" in tool_input:
                        file_name=tool_input["filename"]
                     elif "file_to_write" in tool_input:
                        file_name=tool_input["file_to_write"]
                     else:
                        print("Error: Missing filename in write_file input")
                        file_name="output.txt"
                     content=tool_input["content"]
                     output=avaiable_tools[tool_name]["fn"](file_name,content)
                else:
                    output = avaiable_tools[tool_name]["fn"](tool_input)
                    messages.append(
                        types.Content(
                            role="assistant",
                            parts=[types.Part.from_text(text=json.dumps({"step": "observe", "output": output}))]
                        )
                    )
                    continue

             if parsed_output.get("step") == "output":
                print(f"🤖: {parsed_output.get('content')}")
                break
