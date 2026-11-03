# Task 2: describe a tool
#
# Describe one tool yourself, in the request's list of tools:
#
#   name:        get_quote
#   description: one sentence on what it does
#   parameters:  one required parameter, job, of type string
#
# Send lab-chat the same system message as task 1, and the
# user's question, exactly:
#
#   How much does a tap repair cost?
#
# with your tool. Print three lines:
#
#   1. the first choice's finish reason
#   2. the name of the tool the model asked for
#   3. the call's arguments, as a Python dictionary
#
# Careful: the arguments arrive as a string of JSON text, not
# a dictionary.
#
# Stuck? Press "What do I do next?" under this task. Write
# your code below.
import json

from openai import OpenAI

client = OpenAI()
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_quote",
            "description": "Get the price of a job from GharFix's rate card.",
            "parameters": {
                "type": "object",
                "properties": {"job": {"type": "string", "description": "The job's id on the rate card, like tap-repair"}},
                "required": ["job"],
            },
        },
    }
]
response = client.chat.completions.create(
    model="lab-chat",
    messages=[
        {"role": "system", "content": "You are GharFix's booking assistant. Today is 2026-10-22."},
        {"role": "user", "content": "How much does a tap repair cost?"},
    ],
    tools=tools,
)
choice = response.choices[0]
call = choice.message.tool_calls[0]
print(choice.finish_reason)
print(call.function.name)
print(json.loads(call.function.arguments))
