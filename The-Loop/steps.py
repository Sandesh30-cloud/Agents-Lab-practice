# Task 2: watch each step
#
# Run Meenakshi's job J09 through the loop, exactly:
#
#   Book a carpenter in Bellandur 29 Oct morning: I need a
#   new wardrobe assembled. I am Priya Rao, phone
#   9515819658.
#   (one line, as in the task)
#
# with a system message like task 1's and gharfix.TOOLS.
# For every request, print one line:
#
#   step <n>: <finish reason> <tool names>, <n> prompt tokens
#
# For another job, the lines were:
#
#   step 1: tool_calls find_technicians, 963 prompt tokens
#   step 2: tool_calls book_slot, 1090 prompt tokens
#   step 3: stop, 1318 prompt tokens
#
# Several names: a comma and a space between them. Then
# print the model's final answer.
#
# Careful: the prompt tokens are in the response's usage,
# not in the message.
#
# Stuck? Press "What do I do next?" under this task. Write
# your code below.
import json

from openai import OpenAI

import gharfix

REQUEST = "Book a carpenter in Bellandur 29 Oct morning: I need a new wardrobe assembled. I am Priya Rao, phone 9515819658."

client = OpenAI()
messages = [
    {"role": "system", "content": "You are GharFix's booking assistant in Bengaluru. Today is 2026-10-22. Use the tools."},
    {"role": "user", "content": REQUEST},
]
for step in range(1, 11):
    response = client.chat.completions.create(model="lab-chat", messages=messages, tools=gharfix.TOOLS)
    choice = response.choices[0]
    names = [call.function.name for call in choice.message.tool_calls or []]
    line = f"step {step}: {choice.finish_reason}"
    if names:
        line += " " + ", ".join(names)
    print(f"{line}, {response.usage.prompt_tokens} prompt tokens")
    if choice.finish_reason == "stop":
        print(choice.message.content)
        break
    messages.append(choice.message)
    for call in choice.message.tool_calls:
        result = gharfix.FUNCTIONS[call.function.name](**json.loads(call.function.arguments))
        messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
