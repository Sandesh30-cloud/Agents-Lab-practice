# Task 4 (interview question): the loop that answers one call
#
# A customer asks about two bookings in one message. Run it
# with python3 fix_first_only.py: the API refuses the second
# request. Read which call id it names, then run lab steps
# to see what the model asked for in its first reply.
#
# Fix the loop so that every call in a reply gets its own
# tool message, with its own id and its own result, before
# the next request.
#
# Keep run_agent(question), the system message, the
# customer's message and the one answer it prints.
#
# Careful: the loop worked for every customer who asked one
# thing at a time. That is why nobody noticed.
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


print(run_agent("Are GF894117 and GF990001 both confirmed?"))
