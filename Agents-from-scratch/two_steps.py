# Task 4 (interview question): an agent by hand
#
# Offer lab-chat GharFix's tools (gharfix.TOOLS), with the
# same system message as task 1 and Meenakshi's next
# request, exactly:
#
#   Book an electrician in Jayanagar on 24 Oct, evening. The
#   MCB keeps tripping. I am Divya Menon, phone 9811122233.
#   (one line, as in the task)
#
# A booking needs two tools, one after the other. Each time
# the model asks for tools:
#
#   - run every call with GharFix's function
#   - print the tool's name
#   - send the results back, and ask again
#
# When the model answers in text, print that answer and
# stop. Never send more than 5 requests.
#
# Careful: the first result is not the end. The model reads
# it and asks for the next tool.
#
# Stuck? Press "What do I do next?" under this task. Write
# your code below.
import json

from openai import OpenAI

import gharfix

REQUEST = "Book an electrician in Jayanagar on 24 Oct, evening. The MCB keeps tripping. I am Divya Menon, phone 9811122233."

client = OpenAI()
messages = [
    {"role": "system", "content": "You are GharFix's booking assistant. Today is 2026-10-22."},
    {"role": "user", "content": REQUEST},
]
for _ in range(5):
    response = client.chat.completions.create(model="lab-chat", messages=messages, tools=gharfix.TOOLS)
    message = response.choices[0].message
    if not message.tool_calls:
        print(message.content)
        break
    messages.append(message)
    for call in message.tool_calls:
        print(call.function.name)
        result = gharfix.FUNCTIONS[call.function.name](**json.loads(call.function.arguments))
        messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
