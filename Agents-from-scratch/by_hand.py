# Task 3: one tool call by hand
#
# Vikram's team has described GharFix's booking system as
# eight tools: import gharfix, and use gharfix.TOOLS.
# gharfix.FUNCTIONS maps each tool's name to its function.
#
# Send lab-chat the same system message as task 1, the
# user's question, exactly:
#
#   What does it cost to fix a ceiling fan?
#
# and tools=gharfix.TOOLS. Then:
#
#   1. run each tool call the model asks for, with GharFix's
#      own function and the model's arguments
#   2. send a second request: the conversation so far, the
#      model's own message, and one tool message per call
#      with the result as JSON
#   3. print only the text of the model's final answer
#
# Careful: the model ran nothing. Your code runs the tool.
#
# Stuck? Press "What do I do next?" under this task. Write
# your code below.
import json

from openai import OpenAI

import gharfix

client = OpenAI()
messages = [
    {"role": "system", "content": "You are GharFix's booking assistant. Today is 2026-10-22."},
    {"role": "user", "content": "What does it cost to fix a ceiling fan?"},
]
response = client.chat.completions.create(model="lab-chat", messages=messages, tools=gharfix.TOOLS)
message = response.choices[0].message
messages.append(message)
for call in message.tool_calls:
    result = gharfix.FUNCTIONS[call.function.name](**json.loads(call.function.arguments))
    messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
final = client.chat.completions.create(model="lab-chat", messages=messages, tools=gharfix.TOOLS)
print(final.choices[0].message.content)
