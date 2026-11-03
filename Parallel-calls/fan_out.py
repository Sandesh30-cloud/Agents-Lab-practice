# Task 3: count the calls per step
#
# Run this request through the loop (chapter 3), with the
# same kind of system message and gharfix.TOOLS, exactly:
#
#   Book an electrician in BTM Layout on 27 Oct: a switch is
#   sparking. I am Rekha Nair, phone 9741234567.
#   (one line, as in the task)
#
# Run it twice: first as it is, then with
# parallel_tool_calls=False in every request. Call
# gharfix.reset() between the two runs, so the second one
# starts from the same data. For each run print one line:
#
#   parallel on: 1, 2, 1 calls, 4 requests, 5100 prompt tokens
#   parallel off: ...
#
# (illustrative numbers): the number of calls in each reply
# that asked for tools, in order, then the number of
# requests, then the prompt tokens of all its requests added
# up.
#
# Careful: the first run booked a slot. Without the reset,
# the second run sees it taken.
#
# Stuck? Press "What do I do next?" under this task. Write
# your code below.
import json

from openai import OpenAI

import gharfix

REQUEST = "Book an electrician in BTM Layout on 27 Oct: a switch is sparking. I am Rekha Nair, phone 9741234567."

client = OpenAI()


def run(**options):
    messages = [
        {"role": "system", "content": "You are GharFix's booking assistant in Bengaluru. Today is 2026-10-22. Use the tools."},
        {"role": "user", "content": REQUEST},
    ]
    counts, requests, tokens = [], 0, 0
    while requests < 10:
        response = client.chat.completions.create(model="lab-chat", messages=messages, tools=gharfix.TOOLS, **options)
        requests += 1
        tokens += response.usage.prompt_tokens
        message = response.choices[0].message
        if response.choices[0].finish_reason == "stop":
            break
        counts.append(len(message.tool_calls))
        messages.append(message)
        for call in message.tool_calls:
            result = gharfix.FUNCTIONS[call.function.name](**json.loads(call.function.arguments))
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
    return f"{', '.join(map(str, counts))} calls, {requests} requests, {tokens} prompt tokens"


print("parallel on:", run())
gharfix.reset()
print("parallel off:", run(parallel_tool_calls=False))
