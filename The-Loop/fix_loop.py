# Task 4 (interview question): fix the loop
#
# Meenakshi's team tried this agent on two customers in a
# row. Run it with python3 fix_loop.py: it stops with an
# error from the API at its second request. Read the error,
# then run lab steps to see what each request held.
#
# Fix it so that:
#
#   - every request is one the API accepts: the model's own
#     message with its calls, then one tool message per call
#   - each customer's run starts from its own conversation:
#     the system message and that customer's message only
#
# Keep run_agent(question), the system message, the two
# customers' messages, and the two answers it prints.
#
# Careful: there are two problems. After you fix the first,
# look at the second customer's first request in lab steps:
# how many messages does it hold, and whose are they?
#
# Stuck? Press "What do I do next?" under this task.
import json

from openai import OpenAI

import gharfix

client = OpenAI()


def run_agent(question):
    messages = [
        {"role": "system", "content": "You are GharFix's booking assistant in Bengaluru. Today is 2026-10-22. Use the tools."},
        {"role": "user", "content": question},
    ]
    for _ in range(10):
        response = client.chat.completions.create(model="lab-chat", messages=messages, tools=gharfix.TOOLS)
        message = response.choices[0].message
        if response.choices[0].finish_reason == "stop":
            return message.content
        messages.append(message)
        for call in message.tool_calls:
            result = gharfix.FUNCTIONS[call.function.name](**json.loads(call.function.arguments))
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
    return None


print(run_agent("Book an electrician in Indiranagar 24 Oct evening: the MCB keeps tripping. I am Pooja Prasad, phone 9424438486."))
print(run_agent("Cancel GF114991 and tell me how much I get back."))
