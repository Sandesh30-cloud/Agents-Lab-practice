# Task 3: a model that gets it wrong, then right
#
# Run Meenakshi's job J11 through the loop with the model
# lab-chat-confused, a system message like task 2's,
# gharfix.TOOLS and your run_tool for every call, exactly:
#
#   Book a carpenter in RT Nagar 27 Oct evening: a cupboard
#   hinge came off. I am Deepa Shetty, phone 9992578190.
#   (one line, as in the task)
#
# Its first call has a wrong argument. Send the error back
# as that call's result; the model reads it and asks again.
# When it answers, print the answer, then:
#
#   Requests: N
#
# with the number of requests the run took (at most 10).
#
# Careful: a TypeError that escapes your loop ends the run
# with no booking and no answer.
#
# Stuck? Press "What do I do next?" under this task. Write
# your code below.
from openai import OpenAI

import gharfix
from run_tool import run_tool

client = OpenAI()
messages = [
    {"role": "system", "content": "You are GharFix's booking assistant in Bengaluru. Today is 2026-10-22. Use the tools."},
    {"role": "user", "content": "Book a carpenter in RT Nagar 27 Oct evening: a cupboard hinge came off. I am Deepa Shetty, phone 9992578190."},
]
requests = 0
while requests < 10:
    response = client.chat.completions.create(model="lab-chat-confused", messages=messages, tools=gharfix.TOOLS)
    requests += 1
    message = response.choices[0].message
    if response.choices[0].finish_reason == "stop":
        print(message.content)
        break
    messages.append(message)
    for call in message.tool_calls:
        messages.append({"role": "tool", "tool_call_id": call.id, "content": run_tool(call.function.name, call.function.arguments)})
print(f"Requests: {requests}")
