# Task 3: the run as a transcript
#
# Run Meenakshi's job J12 through the loop, exactly:
#
#   Book an electrician in BTM Layout 30 Oct evening: the
#   geyser is not heating. I am Akshay Sharma, phone
#   9670169067.
#   (one line, as in the task)
#
# with a system message like task 1's and gharfix.TOOLS.
# Keep the final answer in the conversation as its last
# message. Then print the conversation, one line per
# message, in order:
#
#   system: <text>          user: <text>
#   assistant: calls find_technicians    (tool calls; names
#                                         joined with ", ")
#   tool: <the first 60 characters of its text>
#   assistant: <text>                    (the answer)
#
# Careful: the model's messages are objects and yours are
# dictionaries. Store them all in one shape.
#
# Stuck? Press "What do I do next?" under this task. Write
# your code below.
import json

from openai import OpenAI

import gharfix

REQUEST = "Book an electrician in BTM Layout 30 Oct evening: the geyser is not heating. I am Akshay Sharma, phone 9670169067."

client = OpenAI()
messages = [
    {"role": "system", "content": "You are GharFix's booking assistant in Bengaluru. Today is 2026-10-22. Use the tools."},
    {"role": "user", "content": REQUEST},
]
for _ in range(10):
    response = client.chat.completions.create(model="lab-chat", messages=messages, tools=gharfix.TOOLS)
    message = response.choices[0].message
    messages.append(message.model_dump(exclude_none=True))
    if response.choices[0].finish_reason == "stop":
        break
    for call in message.tool_calls:
        result = gharfix.FUNCTIONS[call.function.name](**json.loads(call.function.arguments))
        messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})

for m in messages:
    if m.get("tool_calls"):
        names = ", ".join(c["function"]["name"] for c in m["tool_calls"])
        print(f"assistant: calls {names}")
    elif m["role"] == "tool":
        print(f"tool: {m['content'][:60]}")
    else:
        print(f"{m['role']}: {m['content']}")
